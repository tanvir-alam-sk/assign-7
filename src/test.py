import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.support import expected_conditions as EC

# Configuration
TEST_URL = "https://www.alojamiento.io/"  
OUTPUT_FILE = "../results/results.xlsx" 


# Set up WebDriver using WebDriverManager
def setup_driver():
    options = Options()
    options.add_argument("--headless")  # Run browser in headless mode (no UI)
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration (optional)
    # Use WebDriverManager to get the appropriate chromedriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Scrape all links from the main page
def scrape_all_links(driver):
    links = set()
    try:
        elements = driver.find_elements(By.TAG_NAME, "a")
        for element in elements:
            href = element.get_attribute("href")
            if href and href.startswith(TEST_URL):
                links.add(href)
    except Exception as e:
        print(f"Error scraping links: {e}")
    return list(links)

# Test: Validate H1 tag existence
def validate_h1_tag(driver):
    try:
        h1_tag = driver.find_element(By.TAG_NAME, "h1")
        return "Pass", ""
    except Exception as e:
        return "Fail", f"H1 tag missing: {e}"

# Test: Validate HTML tag sequence (H1-H6)
def validate_html_sequence(driver):
    try:
        tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
        found = [bool(driver.find_elements(By.TAG_NAME, tag)) for tag in tags]
        if found != sorted(found, reverse=True):
            return "Fail", "HTML tag sequence broken"
        return "Pass", ""
    except Exception as e:
        return "Fail", f"Error validating HTML sequence: {e}"

# Test: Validate image alt attributes
def validate_image_alt(driver):
    try:
        images = driver.find_elements(By.TAG_NAME, "img")
        missing_alt = [img for img in images if not img.get_attribute("alt")]
        return ("Pass", "") if not missing_alt else ("Fail", "Some images missing alt attributes")
    except Exception as e:
        return "Fail", f"Error validating image alt attributes: {e}"

# Test: Validate URL status codes
def validate_url_status(driver):
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        broken_links = []
        for link in links:
            url = link.get_attribute("href")
            if url:
                try:
                    response = requests.head(url, timeout=10)  # Adjust timeout
                    if response.status_code == 404:
                        broken_links.append(url)
                except requests.exceptions.RequestException as e:
                    broken_links.append(url)
        if not broken_links:
            return "Pass", ""
        else:
            return "Fail", f"Broken URLs: {', '.join(broken_links)}"
    except Exception as e:
        return "Fail", f"Error validating URL status: {e}"

# Test: Validate currency filter
def validate_currency_filter(driver):
    try:
        # Wait for currency selector to be visible
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "currency-selector")))
        currency_select = driver.find_element(By.ID, "currency-selector")  
        options = currency_select.find_elements(By.TAG_NAME, "option")
        if not options:
            return "Fail", "No currency options available"
        options[1].click()  # Change to another currency
        # Wait for property prices to update
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "price")))
        property_prices = driver.find_elements(By.CLASS_NAME, "price")
        changed = all("$" in price.text for price in property_prices)  # Check if symbol changed
        return "Pass", "" if changed else "Fail", "Currency did not change correctly"
    except Exception as e:
        return "Fail", f"Error validating currency filter: {e}"

# Write results to Excel
def write_to_excel(results, file_name):
    try:
        df = pd.DataFrame(results, columns=["page_url", "testcase", "passed/fail", "comments"])
        df.to_excel(file_name, index=False)
    except Exception as e:
        print(f"Error writing to Excel: {e}")



# Main function
def main():
    driver = setup_driver()
    driver.get(TEST_URL)
    
    # Wait for the page to load completely (you can adjust this as per the website)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "a")))  # Wait for links to load
    
    all_links = scrape_all_links(driver)  

    results = []

    for link in all_links:
        print(f"Testing page: {link}")
        driver.get(link)
        
        # Wait for page to load before running tests
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

        # Perform tests and record results
        for test_name, test_function in [
            ("H1 Tag Existence", validate_h1_tag),
            ("HTML Tag Sequence", validate_html_sequence),
            ("Image Alt Attribute", validate_image_alt),
            ("URL Status Codes", validate_url_status),
            ("Currency Filter", validate_currency_filter),
        ]:
            result, comment = test_function(driver)
            results.append({
                "page_url": link,
                "testcase": test_name,
                "passed/fail": result,
                "comments": comment
            })

    # Save results to Excel
    write_to_excel(results, OUTPUT_FILE)
    driver.quit()
    print(f"Test results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
