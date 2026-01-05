## Sales Data Processing

Runs data processing on sale CSV files using the predetermined schema. Exports to Excel/Sheets for further analysis and/or visualization.

Uses environment variables and a Google Service account for Google Sheets authentication. To use the upload function, these must be personalized.

### Modules
- add_sales_features.py
    - Adds a field for days listed on platform
    - Flags sales surges
        - UUses a rolling 7-day baseline, flagging days with >100% increases & accounting for periods with no prior sales.
    - Description sentiment: 
        - Adds detected sentiment class and confidence in positive sentiment.
        - Sentiment may or may not be in descriptions; depends on style of seller data.

- anonymize.py
    - Defaults to removing PII columns
    - Optionally uses SHA-256 hashing on specified columns

- data_cleaning.py
    - Removes any potential currency symbols or infinite values

- export_upload.py
    - Optional Google Sheets upload

- file_utils.py
    - Selects input data, optional Excel export

- run_pipeline.py
    - Runs other modules
