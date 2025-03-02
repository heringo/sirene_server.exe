import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def get_driver():
    # Set up Chrome options for headless mode on a Linux server.
    options = Options()
    options.add_argument('--headless')  # Headless mode activated.
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/90.0.4430.93 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    return driver

def search_siren(siren_value, driver=None):
    """
    Searches pappers.fr for the given SIREN value using Selenium by
    simulating a user entering the SIREN in the search box on the homepage.
    
    Parameters:
      - siren_value (str): The SIREN number to search for.
      - driver (webdriver, optional): An existing Selenium webdriver instance.
      
    Returns:
      - A string containing the owner names separated by commas,
        or an empty string if no owner names are found.
    """
    driver_created = False
    if driver is None:
        driver = get_driver()
        driver_created = True

    try:
        # Open the homepage to initialize cookies/session data.
        homepage_url = "https://pappers.fr/"
        driver.get(homepage_url)
        time.sleep(random.uniform(1, 3))

        # Instead of directly constructing a URL, simulate a user search:
        search_input = driver.find_element(By.CSS_SELECTOR, "input[name='q']")
        search_input.clear()
        search_input.send_keys(siren_value)
        search_input.send_keys(Keys.RETURN)
        time.sleep(random.uniform(1, 3))

        # Parse the current page's HTML with BeautifulSoup.
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        name_elements = soup.select("td.info-dirigeant a.underline")

        if name_elements:
            owner_names = [elem.get_text(strip=True) for elem in name_elements if elem.get_text(strip=True)]
            owner_names_str = ", ".join(owner_names)
            print(f"SIREN: {siren_value} | Owner Names: {owner_names_str}")
        else:
            print(f"SIREN: {siren_value} | No owner names found.")
            owner_names_str = ""
    except Exception as e:
        print(f"Error processing SIREN {siren_value}: {e}")
        owner_names_str = ""
    
    if driver_created:
        driver.quit()
    
    return owner_names_str

def pappers_search(siren):
    """
    Searches pappers.fr for the given SIREN(s) using Selenium and returns owner names.
    
    Parameters:
      - siren (str or pd.DataFrame): A single SIREN (as a string) or a DataFrame with a "siren" column.
      
    Returns:
      - If a single SIREN (string) is provided: a string containing the owner names separated by commas,
        or an empty string if no owner names are found.
      - If a DataFrame is provided: a DataFrame with an additional column "owner_names".
    """
    if isinstance(siren, pd.DataFrame):
        # Create one driver to be reused for all searches.
        driver = get_driver()
        results = []
        for idx, row in siren.iterrows():
            single_siren = row["siren"]
            owner_names_str = search_siren(single_siren, driver=driver)
            results.append(owner_names_str)
            time.sleep(random.uniform(1, 3))
        driver.quit()
        return pd.DataFrame({"siren": siren["siren"], "owner_names": results})
    else:
        return search_siren(siren)

if __name__ == "__main__":
    # For a DataFrame of SIRENs:
    df_input = pd.DataFrame({"siren": ["941033094", "941254567", "941175457"]})
    df_result = pappers_search(df_input)
    print("DataFrame result:")
    print(df_result)
