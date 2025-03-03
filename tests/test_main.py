import unittest
import pandas as pd
import sys
import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe
from datetime import datetime

# Load environment variables from the .env file in the config folder.
load_dotenv(os.path.join(os.path.dirname(__file__), '../config/.env'))

# Add the src folder to the module search path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import main  # Ensure your main module is located at src/main.py

class TestRealPipelineWithSendToSheet(unittest.TestCase):
    def test_pipeline_with_sheet(self):
        # 1. Fetch SIREN data (real API call)
        df_siren = main.fetch_lastweek_multi_naf_siege_fields()
        self.assertIsNotNone(df_siren, "fetch_lastweek_multi_naf_siege_fields() returned None.")
        # Limit to the first 3 records for testing.
        df_siren = df_siren.head(3)
        self.assertGreaterEqual(len(df_siren), 3, "Less than 3 records fetched for testing.")

        # 2. Process pappers search on the fetched Siren data.
        df_pappers = main.pappers_search(df_siren)
        self.assertIsInstance(df_pappers, pd.DataFrame, "pappers_search did not return a DataFrame.")
        self.assertIn("owner_names", df_pappers.columns, "Column 'owner_names' missing after pappers_search.")
        for name in df_pappers["owner_names"]:
            self.assertNotEqual(str(name).strip(), "", "Empty owner name returned in pappers_search.")

        # 3. Process LinkedIn search on the pappers result.
        df_linkedin = main.linkedin_search(df_pappers)
        self.assertIsInstance(df_linkedin, pd.DataFrame, "linkedin_search did not return a DataFrame.")
        self.assertIn("linkedin_urls", df_linkedin.columns, "Column 'linkedin_urls' missing after linkedin_search.")
        for url in df_linkedin["linkedin_urls"]:
            self.assertNotEqual(str(url).strip(), "", "Empty LinkedIn URL returned in linkedin_search.")

        final_df = df_linkedin
        print("Final DataFrame after LinkedIn search:")
        print(final_df)

        # 4. Retrieve spreadsheet details from environment variables.
        spreadsheet_id = os.environ.get("SPREADSHEET_ID")
        worksheet_name = "test"  # Required as parameter
        self.assertIsNotNone(spreadsheet_id, "SPREADSHEET_ID environment variable is not set.")
        self.assertIsNotNone(worksheet_name, "WORKSHEET_NAME environment variable is not set.")

        # 5. Compute the expected worksheet title (as used in send_df_to_gsheet).
        expected_sheet_title = f"Greffe_week_{datetime.now().strftime('%Y%m%d')}"

        # 6. Send the final DataFrame to Google Sheets using the real function.
        main.send_df_to_gsheet(final_df, spreadsheet_id, worksheet_name)
        print("Data sent to Google Sheets.")

        # 7. Use gspread to read back the data from the newly created worksheet.
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(
            os.path.join(os.path.dirname(__file__), '../config/service_account.json'),
            scopes=scopes
        )
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(spreadsheet_id)
        # The send_df_to_gsheet function creates a new worksheet with a unique title.
        worksheet = sheet.worksheet(expected_sheet_title)

        # Read the worksheet data into a DataFrame.
        read_df = get_as_dataframe(worksheet, evaluate_formulas=True, dtype=str)
        read_df.dropna(how='all', inplace=True)
        read_df.reset_index(drop=True, inplace=True)
        print("Data read from Google Sheets:")
        print(read_df)

        # Verify that the expected columns are present in the sheet data.
        for col in final_df.columns:
            self.assertIn(col, read_df.columns, f"Column '{col}' is missing in the sheet data.")

if __name__ == "__main__":
    unittest.main()
