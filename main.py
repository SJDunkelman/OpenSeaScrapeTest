from bs4 import BeautifulSoup as bs4
from selenium import webdriver
import os
import shutil

# Web driver paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_DRIVER_PATH = ""  # REPLACE WITH USER CHROME WEB DRIVER EXECUTABLE PATH
CHROME_BINARY_PATH = ""  # REPLACE WITH USER CHROME APPLICATION PATH


def open_selenium_driver():
    # Delete existing chrome-data dir
    chrome_data_dir = f"{ROOT_DIR}/chrome-data"
    if os.path.isdir(chrome_data_dir):
        try:
            shutil.rmtree(chrome_data_dir)
        except OSError as e:
            print("Error: %s : %s" % (chrome_data_dir, e.strerror))

    options = webdriver.ChromeOptions()
    options.binary_location = CHROME_BINARY_PATH
    options.add_argument("--user-data-dir=chrome-data")
    options.add_argument('--no-sandbox')
    return webdriver.Chrome(CHROME_DRIVER_PATH, options=options)


test_url = 'https://opensea.io/activity/pudgypenguins?search[isSingleCollection]=true&search[eventTypes][0]=AUCTION_SUCCESSFUL'
unit_price_class = 'Price--amount'

if __name__ == "__main__":
    driver = open_selenium_driver()
    driver.get(test_url)
    html = driver.page_source.encode("utf-8")
    soup = bs4(html, 'html.parser')
    price_divs = soup.find_all('div', {'class': unit_price_class})
    for p in price_divs:
        print(float(p.text))
