"""
Anonymizes sales data by removing personally identifiable information (PII) from a CSV file.
The script reads a CSV file, removes specified PII columns, and saves the anonymized data to a new CSV file.
"""

import pandas as pd
import hashlib




def anonymize_sales_data(df, pii_columns):
    # drops PII columns
    df = df.copy()
    df.drop(columns=pii_columns, errors='ignore', inplace=True)
    return df



def hash_pii_columns(df, pii_columns):
    # hashes PII columns
    df = df.copy()
    for col in pii_columns:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: hashlib.sha256(str(x).encode()).hexdigest() if pd.notnull(x) else x
            )
    return df






def run_anonymization(df):
    """Anonymizes the cleaned sales DataFrame by removing or hashing PII columns. Returns the anonymized DataFrame."""

    pii_columns_to_remove = ["Name", "Address Line 1", "Address Line 2", "City", "Post Code", "Buyer"]

    
    if pii_columns_to_remove:
        df = anonymize_sales_data(df, pii_columns_to_remove)

    hash_columns = []
    if hash_columns:
        df = hash_pii_columns(df, hash_columns)

    return df
    

