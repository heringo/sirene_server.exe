import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import pandas as pd
from datetime import datetime

def send_df_to_gsheet(df, spreadsheet_id, worksheet_name):
    """
    Sends the provided DataFrame to a new worksheet in the specified Google Spreadsheet.
    A unique worksheet is created each time using a timestamp appended to the given worksheet_name,
    along with the phrase "the_week" in the title.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to send.
        spreadsheet_id (str): The ID of the Google Spreadsheet.
        worksheet_name (str): The base name for the new worksheet.
    """
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']
    
    credentials = Credentials.from_service_account_file("service_account.json", scopes=scopes)
    client = gspread.authorize(credentials)
    
    sheet = client.open_by_key(spreadsheet_id)
    
    # Create a new unique worksheet title by appending "the_week" and the current timestamp.
    unique_title = f"Greffe_week_{datetime.now().strftime('%Y%m%d')}"
    worksheet = sheet.add_worksheet(title=unique_title, rows="100", cols="20")
    
    # Write the DataFrame to the new worksheet
    set_with_dataframe(worksheet, df)
    print(f"DataFrame successfully sent to new worksheet: {unique_title}")

if __name__ == "__main__":
    data = {
        "siren": [123456789, 987654321],
        "owner_names": ["John Doe", "Alice Johnson"],
        "linkedin_urls": ["https://www.linkedin.com/in/johndoe", "https://www.linkedin.com/in/alicejohnson"]
    }
    df = pd.DataFrame(data)
    
    # # Replace with your actual Spreadsheet ID and desired base worksheet name.
    # SPREADSHEET_ID = "your_spreadsheet_id"
    # WORKSHEET_NAME = "Sheet1"
    
    # send_df_to_gsheet(df, SPREADSHEET_ID, WORKSHEET_NAME)
