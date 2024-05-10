import os
import time
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

# Directory to save extracted documentation
output_dir = '/home/amuller/Documents/mirinae/lookup/coin_market/docs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Path to the file containing URLs
input_path = '/home/amuller/Documents/mirinae/lookup/coin_market/urls.txt'

# Function to extract the relevant API documentation
def extract_documentation(url):
    try:
        # Load the page with Selenium
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "api-info-wrapper"))
        )

        # Extract the fully rendered page's content
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract text while preserving headings and sub-sections
        doc_content = []
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li']):
            if tag.name in ['h1', 'h2', 'h3', 'h4']:
                doc_content.append('\n\n' + tag.text.strip().upper() + '\n')
            else:
                doc_content.append(tag.text.strip())

        return '\n'.join(filter(None, doc_content))

    except Exception as e:
        print(f"Error processing {url}: {e}")
        return ""

def safe_filename(url):
    """Generate a safe filename from a URL."""
    section_identifier = url.split('#')[-1] if '#' in url else 'main_content'
    return section_identifier.replace('/', '_').replace('\\', '_') + '.txt'

if __name__ == '__main__':
    with open(input_path, 'r') as f:
        for url in f:
            url = url.strip()
            if url:
                try:
                    print(f"Processing {url}...")
                    doc_content = extract_documentation(url)
                    if doc_content:
                        file_name = safe_filename(url)
                        with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as text_file:
                            text_file.write(doc_content)
                except Exception as e:
                    print(f"Error processing {url}: {e}")

    print(f"Documentation data saved in {output_dir}")

# Close the Selenium driver when done
driver.quit()
