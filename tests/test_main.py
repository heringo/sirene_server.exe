import unittest
import pandas as pd
import sys
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env dans le dossier config
load_dotenv(os.path.join(os.path.dirname(__file__), '../config/.env'))

# Ajouter le dossier src au chemin de recherche des modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import main  # Assurez-vous que votre module principal est situé dans src/main.py

class TestRealPipeline(unittest.TestCase):
    def test_pipeline(self):
        # 1. Fetch Siren data (real API call)
        df_siren = main.fetch_lastweek_multi_naf_siege_fields()
        self.assertIsNotNone(df_siren, "fetch_lastweek_multi_naf_siege_fields() returned None.")
        # Limit to the first 3 rows for testing
        df_siren = df_siren.head(3)
        self.assertGreaterEqual(len(df_siren), 3, "Not enough Siren rows returned for testing.")

        # 2. Run pappers search on the fetched Siren data.
        df_pappers = main.pappers_search(df_siren)
        self.assertIsInstance(df_pappers, pd.DataFrame, "pappers_search did not return a DataFrame.")
        self.assertIn("owner_names", df_pappers.columns, "owner_names column is missing after pappers_search.")
        for name in df_pappers["owner_names"]:
            self.assertNotEqual(name.strip(), "", "pappers_search returned an empty owner name for a Siren.")

        # 3. Run LinkedIn search on the pappers result.
        df_linkedin = main.linkedin_search(df_pappers)
        self.assertIsInstance(df_linkedin, pd.DataFrame, "linkedin_search did not return a DataFrame.")
        self.assertIn("linkedin_urls", df_linkedin.columns, "linkedin_urls column is missing after linkedin_search.")
        for url in df_linkedin["linkedin_urls"]:
            self.assertNotEqual(url.strip(), "", "linkedin_search returned an empty URL for an owner.")

        # Optionally, print the resulting DataFrame for manual inspection.
        print("Final DataFrame from LinkedIn search:")
        print(df_linkedin)

if __name__ == "__main__":
    unittest.main()
