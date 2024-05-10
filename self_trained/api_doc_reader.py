from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up the WebDriver
options = webdriver.ChromeOptions()
options.headless = True  # Run in headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load the main page and wait for the content to load
BASE_URL = 'https://coinmarketcap.com/api/documentation/v1/'
driver.get(BASE_URL)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.share-link")))

# Parse the loaded page with BeautifulSoup
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Function to extract all hrefs within the 'a.share-link'
def extract_links():
    links = []
    for anchor in soup.find_all('a', class_='share-link'):
        href = anchor.get('href')
        if href:
            full_url = BASE_URL + href.lstrip('/')
            links.append(full_url)
    return links

# Extract the share-link hrefs
share_links = extract_links()

# Save the links to a text file
output_path = '/home/amuller/Documents/mirinae/lookup/self_trained/api_doc.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    for link in share_links:
        f.write(link + '\n')

print(f"Share links saved to {output_path}")

# Close the driver
driver.quit()
