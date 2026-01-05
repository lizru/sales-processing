import pandas as pd

def clean_prices(df, price_cols):
    # cleans price columns by removing currency symbols and converting to float
    df = df.copy()
    for col in price_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace(r'[\$,\-=]', '', regex=True)
            df[col] = df[col].replace(r'^\s*$', '0', regex=True) # whitespace to 0
            df[col] = df[col].replace(r'^""$', '0', regex=True)  
            df[col] = df[col].astype(float)

    return df

def clean_df(df):
    # cleans the DataFrame by replacing infinite values and filling NaNs
    df = df.copy()
    price_cols=["Item price", "Buyer shipping cost", "Total", "USPS Cost", "Depop fee", "Depop Payments fee", 
                "Buyer Marketplace Fee", "Boosting fee", "US Sales tax", "Refunded to buyer amount", "Fees refunded to seller"]

    df = clean_prices(df, price_cols)
    df = df.replace([float('inf'), float('-inf')], pd.NA)
    return df




