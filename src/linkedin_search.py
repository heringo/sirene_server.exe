import time
import random
import os
from dotenv import load_dotenv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables from your .env file (make sure it is in your .gitignore)
load_dotenv()

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

if not EMAIL or not PASSWORD:
    raise ValueError("Please set the EMAIL and PASSWORD environment variables in your .env file.")

def linkedin_search(input_df):
    """
    Takes a DataFrame with a column 'owner_names' (owner names can be comma-separated if multiple)
    and returns a DataFrame with an additional column 'linkedin_urls' containing the LinkedIn profile URL(s)
    found for each owner.
    If no owner names are provided, the research is skipped.
    """
    # Set up the Chrome driver in headless mode.
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Headless mode activated.
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)
    
    # Login to LinkedIn with extra delays.
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(EMAIL)
    time.sleep(random.uniform(1, 2))
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    time.sleep(random.uniform(1, 2))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(random.uniform(3, 5))
    
    # Wait for the search bar on the homepage to be available.
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search')]"))
    )
    
    linkedin_results = []
    
    # Iterate over each row in the input DataFrame.
    for idx, row in input_df.iterrows():
        owner_names_str = row.get("owner_names", "")
        if not owner_names_str:
            print(f"SIREN: {row.get('siren', 'N/A')} | No owner names found. Skipping LinkedIn search.")
            linkedin_results.append("")
            continue
        
        # If there are multiple owner names, split by comma.
        owner_names_list = [name.strip() for name in owner_names_str.split(",") if name.strip()]
        owner_urls = []
        
        for name in owner_names_list:
            try:
                # Locate the search bar and clear any previous input.
                search_box = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Search')]")
                search_box.clear()
                time.sleep(random.uniform(1, 2))
                search_box.send_keys(name)
                time.sleep(random.uniform(1, 2))
                search_box.send_keys(Keys.RETURN)
                time.sleep(random.uniform(1, 2))
                
                # Wait for the search results page to load.
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-results-container')]"))
                )
                time.sleep(random.uniform(1, 2))
                
                # Click the "People" tab if available to filter the results.
                try:
                    people_tab = driver.find_element(By.XPATH, "//button[contains(., 'People')]")
                    people_tab.click()
                    time.sleep(random.uniform(2, 4))
                except Exception as e:
                    print(f"People tab not found for {name}: {e}")
                
                # Wait for people results to load.
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@data-test-app-aware-link and contains(@href, '/in/')]"))
                )
                time.sleep(random.uniform(0.5, 1.5))
                
                # Get the first profile result URL.
                first_profile = driver.find_element(By.XPATH, "//a[@data-test-app-aware-link and contains(@href, '/in/')]")
                profile_url = first_profile.get_attribute("href")
                owner_urls.append(profile_url)
                print(f"Found LinkedIn URL for {name}: {profile_url}")
            except Exception as e:
                print(f"Error retrieving LinkedIn URL for {name}: {e}")
                owner_urls.append("")
            finally:
                # Return to the LinkedIn homepage (feed) for the next search.
                driver.get("https://www.linkedin.com/feed/")
                time.sleep(random.uniform(1.5, 3))
        
        # Combine all URLs found for the current row into a single string.
        linkedin_results.append(", ".join(owner_urls))
    
    driver.quit()
    input_df["linkedin_urls"] = linkedin_results
    return input_df

if __name__ == "__main__":
    # Example input DataFrame with a 'siren' and 'owner_names' column.
    data = {
        "siren": ["123456789", "987654321"],
        "owner_names": ["John Doe, Jane Smith", ""]  # Second row has no owner names; LinkedIn search will be skipped.
    }
    df_input = pd.DataFrame(data)
    
    # Search LinkedIn for the provided owner names.
    df_output = linkedin_search(df_input)
    print(df_output)
