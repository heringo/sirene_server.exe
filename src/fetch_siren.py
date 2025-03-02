import os
import requests
from datetime import datetime, timedelta
import pandas as pd

SIREN_API = os.environ.get("SIREN_API")


def fetch_lastweek_multi_naf_siege_fields():
    # 1) Liste des codes NAF
    naf_codes = [
        "58.29C", 
        "58.29A", 
        "62.01Z", 
        "62.02A", 
        "63.12Z", 
        "63.11Z"
    ]

    # Calculate key dates
    current_date = datetime.utcnow()  # Use UTC time
    # Get the Monday of the current week
    current_week_monday = current_date - timedelta(days=current_date.weekday())
    # Last week: Monday to Sunday
    last_week_monday = current_week_monday - timedelta(days=7)
    last_week_sunday = last_week_monday + timedelta(days=6)
    
    # For dateCreationUniteLegale: we want the period from two weeks ago (last week's Monday minus 7 days)
    # to last week's Sunday.
    creation_start_date = (last_week_monday - timedelta(days=14)).strftime("%Y-%m-%d")
    creation_end_date = last_week_sunday.strftime("%Y-%m-%d")
    
    # For the last update date: we want only last week.
    update_start_date = last_week_monday.strftime("%Y-%m-%d")
    update_end_date = last_week_sunday.strftime("%Y-%m-%d")
    
    # Build the NAF query (using OR between codes)
    naf_queries = [f"periode(activitePrincipaleUniteLegale:{code})" for code in naf_codes]
    combined_naf_query = " OR ".join(naf_queries)
    
    # Construct the full query with two date filters:
    # - The creation date filter: dateCreationUniteLegale from two weeks ago to last week.
    # - The last update filter: dateDerniereMiseAJourUniteLegale only during last week.
    full_query = (
        f"({combined_naf_query}) AND "
        f"dateCreationUniteLegale:[{creation_start_date} TO {creation_end_date}] AND "
        f"dateDernierTraitementUniteLegale:[{update_start_date} TO {update_end_date}]"
    )
    
    url = "https://api.insee.fr/api-sirene/3.11/siren"
    
    params = {
        "q": full_query,
        "nombre": 2000,
        "debut": 0
    }
    
    headers = {
        "X-INSEE-Api-Key-Integration": SIREN_API
    }
    
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = []
        for unite_legale in data.get("unitesLegales", []):
            siren = unite_legale.get("siren")
            results.append({"siren": siren})
        return pd.DataFrame(results)
    else:
        print(f"Erreur HTTP {response.status_code}")
        print("Contenu :", response.text)
        return None

if __name__ == "__main__":
    data = fetch_lastweek_multi_naf_siege_fields()
    if data is not None:
        df = pd.DataFrame(data)
        print(f"Nombre d'unités légales trouvées : {len(df)}\n")
        print(df.head())
