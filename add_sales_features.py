import pandas as pd
import datetime as dt
from scipy.stats import zscore
import numpy as np


# Load model directly
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")

def find_time_to_sell(df, list_date='Date of listing', sold_date='Date of sale'):
    """Returns a df with new field 'Days listed'."""
    df = df.copy()
    df[list_date] = pd.to_datetime(df[list_date])
    df[sold_date] = pd.to_datetime(df[sold_date])
    df['Days listed'] = (df[sold_date] - df[list_date]).dt.days
    return df




def detect_surge(df, date_col='Date of sale', z_threshold=2):
    """Returns a df with new field 'Surge sale' indicating if the number of sales is above the threshold times the average sales for that month."""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df['YearMonth'] = df[date_col].dt.to_period('M')
    monthly_counts = df.groupby('YearMonth').size()
    z = zscore(monthly_counts)
    surge_months = pd.Series(z > z_threshold, index=monthly_counts.index)
    df['Surge sale'] = df['YearMonth'].map(surge_months)
    df.drop(columns=['YearMonth'], inplace=True, errors='ignore')
    return df


def sentiment_analysis(df, text_col = 'Description'):
    """
    Returns a df with new field 'Sentiment' indicating sentiment score of the text column.
    Mapping is -1: negative, 0:1 positive, None.
       """
    def softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)
    
    def analyze_sentiment(text):
        if pd.isna(text) or text.strip() == "":
            return pd.Series([None, None])
        
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        
        scores = outputs[0][0].detach().numpy()  # logits
        probs = softmax(scores)
        sentiment = probs.argmax() - 1           # map 0,1,2 → -1,0,1
        confidence = probs.max()
        
        return pd.Series([sentiment, confidence])
    
    df = df.copy()
    df[['Sentiment', 'Sentiment_confidence']] = df[text_col].apply(analyze_sentiment)
    return df


    
def add_all_sales_features(df):
    """
    Wrapper function, adds sales features to the DataFrame.
    Includes time to sell, surge detection, and description sentiment analysis.
    """
    df = find_time_to_sell(df)
    df = detect_surge(df)
    df = sentiment_analysis(df)
    
    return df