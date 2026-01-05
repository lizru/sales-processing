# Runs the full data processing pipeline of anonymization, feature addition, and saving the final dataset.

import anonymize
import add_sales_features
import file_utils
import data_cleaning

def main():

    
    df = file_utils.select_sales_file_path()
    df = data_cleaning.clean_df(df)
    df = anonymize.run_anonymization(df)
    df = add_sales_features.add_all_sales_features(df)
    file_utils.export_choice_dialog(df)

    
if __name__ == "__main__":
    main()


    