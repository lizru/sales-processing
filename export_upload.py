

from dotenv import load_dotenv
import os
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
import gspread


load_dotenv()
CRED_FILE = os.getenv("CRED_FILE")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")




def upload_to_google_sheet(df, sheet_id=SPREADSHEET_ID, creds_file=CRED_FILE):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file(creds_file, scopes=SCOPES)
    gs_client = gspread.authorize(creds)

    try:
        spreadsheet = gs_client.open_by_key(sheet_id)
    except gspread.SpreadsheetNotFound:
        raise FileNotFoundError("Spreadsheet not found. Check the SPREADSHEET_ID.")

    worksheet = spreadsheet.sheet1
    worksheet.clear()
    set_with_dataframe(worksheet, df)
    print("Upload to Google Sheets completed.")

