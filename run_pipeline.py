"""
Runs the full data processing pipeline: anonymization, feature addition, and saving the final dataset.
Uses anonymize.py and add_sales_features.py modules.
"""

import anonymize
import add_sales_features


def main():
    sales_df = anonymize.run_anonymization()
    print('1')
    sales_df = add_sales_features.add_all_sales_features(sales_df)
    print('2')
    anonymize.upload_to_google_sheet(sales_df)

if __name__ == "__main__":
    main()