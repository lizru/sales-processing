import pandas as pd
from scipy.stats import zscore
import numpy as np
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




def detect_surge(df, date_col='Date of sale', window=7, pct_increase=1.0, min_count=1):
    """Returns a df with new field 'Surge sale' indicating if the sale occurred during a surge period."""
    df = df.copy()

    df[date_col] = pd.to_datetime(df[date_col])
    daily_counts = df.groupby(df[date_col].dt.date).size().rename('daily_sales').sort_index()

    rolling_avg = daily_counts.rolling(window=window, min_periods=1).mean()
    threshold = rolling_avg * (1 + pct_increase)
    
    surge_days = (daily_counts >= threshold) | ((rolling_avg == 0) & (daily_counts >= min_count))
    df['Surge sale'] = df[date_col].dt.date.map(surge_days)
    return df


def sentiment_analysis(df, text_col = 'Description'):
    """
    Returns a df with new fields 'Sentiment' and 'Sentiment_confidence'.
    Mapping is -1: negative, 0:1 positive, None. Confidence is the probability of the positive class.
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
        
        scores = outputs[0][0].detach().numpy()
        probs = softmax(scores)
        
        sentiment = probs.argmax() - 1
        
        # positive prob, index of 2
        pos_prob = probs[2]
        
        return pd.Series([sentiment, pos_prob])
    
    df = df.copy()
    df[['Sentiment', 'Sentiment_confidence']] = df[text_col].apply(analyze_sentiment)
    return df


    
def add_all_sales_features(df):
    """
    Wrapper function
    Includes time to sell, surge detection, and description sentiment analysis.
    """
    df = find_time_to_sell(df)
    df = detect_surge(df)
    df = sentiment_analysis(df)
    
    return df