import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
import main

# Dummy functions for testing

def dummy_fetch_lastweek_multi_naf_siege_fields():
    # Return a dummy DataFrame with a "siren" column.
    # Let's create 6 rows.
    return pd.DataFrame({
        "siren": ["S1", "S2", "S3", "S4", "S5", "S6"]
    })

def dummy_pappers_search(df_chunk):
    # For each row in the chunk, add "owner_names" as "Owner_" + siren.
    df = df_chunk.copy()
    df["owner_names"] = df["siren"].apply(lambda x: "Owner_" + x)
    return df

def dummy_linkedin_search(df_chunk):
    # For each row in the chunk, add "linkedin_urls" as "http://linkedin.com/in/Owner_" + siren.
    df = df_chunk.copy()
    df["linkedin_urls"] = df["siren"].apply(lambda x: "http://linkedin.com/in/Owner_" + x)
    return df

# Global variable to capture the final DataFrame sent to Google Sheets.
global_result = None

def dummy_send_df_to_gsheet(df, spreadsheet_id, worksheet_name):
    global global_result
    global_result = df

class TestMainPipeline(unittest.TestCase):
    def setUp(self):
        # Monkey-patch the external functions in the main module.
        main.fetch_lastweek_multi_naf_siege_fields = dummy_fetch_lastweek_multi_naf_siege_fields
        main.pappers_search = dummy_pappers_search
        main.linkedin_search = dummy_linkedin_search
        main.send_df_to_gsheet = dummy_send_df_to_gsheet

    def test_pipeline(self):
        # Run the main pipeline.
        main.main()

        # Check that the global_result has been set.
        self.assertIsNotNone(global_result, "The final DataFrame was not sent to Google Sheets.")

        # Create the expected DataFrame.
        expected_df = pd.DataFrame({
            "siren": ["S1", "S2", "S3", "S4", "S5", "S6"],
            "owner_names": ["Owner_S1", "Owner_S2", "Owner_S3", "Owner_S4", "Owner_S5", "Owner_S6"],
            "linkedin_urls": [
                "http://linkedin.com/in/Owner_S1",
                "http://linkedin.com/in/Owner_S2",
                "http://linkedin.com/in/Owner_S3",
                "http://linkedin.com/in/Owner_S4",
                "http://linkedin.com/in/Owner_S5",
                "http://linkedin.com/in/Owner_S6"
            ]
        })

        # Reset index for both DataFrames before comparison.
        result_df = global_result.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)

        # Compare the DataFrames.
        assert_frame_equal(result_df, expected_df)

if __name__ == '__main__':
    unittest.main()
