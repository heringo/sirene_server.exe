import os 
import pandas as pd
import concurrent.futures
from fetch_siren import fetch_lastweek_multi_naf_siege_fields
from pappers_search import pappers_search
from linkedin_search import linkedin_search
from to_gsheet import send_df_to_gsheet

MAX_WORKERS = 2  # Maximum number of parallel agents

SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")

def chunkify_df(df, n):
    """Divide DataFrame df into n roughly equal chunks."""
    chunks = []
    chunk_size = len(df) // n
    remainder = len(df) % n
    start = 0
    for i in range(n):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunks.append(df.iloc[start:end])
        start = end
    return chunks

def main():
    # Step 1: Fetch SIREN data from the INSEE API (for last week)
    print("Fetching SIREN data from INSEE API...")
    df_siren = fetch_lastweek_multi_naf_siege_fields()
    if df_siren is None or df_siren.empty:
        print("No SIREN data retrieved. Exiting.")
        return
    print(f"Fetched {len(df_siren)} SIREN records.")

    # Stage 1: Process Pappers search in parallel by splitting the DataFrame into chunks.
    print("Starting Pappers search with multiprocessing...")
    siren_chunks = chunkify_df(df_siren, MAX_WORKERS)
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Each worker processes a chunk of the DataFrame with a single browser session.
        pappers_chunks = list(executor.map(pappers_search, siren_chunks))
    # Concatenate the results from each chunk into one DataFrame.
    df_pappers = pd.concat(pappers_chunks, ignore_index=True)
    print("Pappers search results:")
    print(df_pappers.head())

    # Stage 2: Process LinkedIn search in parallel by splitting the Pappers results into chunks.
    print("Starting LinkedIn search with multiprocessing...")
    pappers_chunks = chunkify_df(df_pappers, MAX_WORKERS)
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        linkedin_chunks = list(executor.map(linkedin_search, pappers_chunks))
    df_final = pd.concat(linkedin_chunks, ignore_index=True)
    print("Final results:")
    print(df_final.head())

    # Save final results to CSV
    df_final.to_csv("final_results.csv", index=False)
    print("Final results saved to 'final_results.csv'.")

    # Step 3: Send the final DataFrame to a new worksheet in Google Sheets
    WORKSHEET_NAME = "Sheet1"  # Base worksheet name; a unique sheet will be created
    send_df_to_gsheet(df_final, SPREADSHEET_ID, WORKSHEET_NAME)

if __name__ == "__main__":
    main()
