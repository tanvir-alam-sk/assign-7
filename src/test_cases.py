import time
import requests
from selenium.webdriver.common.by import By

# Example: Validate H1 tag existence
def validate_h1_tag(driver):
    try:
        h1_tag = driver.find_element(By.TAG_NAME, "h1")
        return "Pass" if h1_tag else "Fail"
    except:
        return "Fail"

# Add other test functions (HTML sequence, image alt, URL validation, etc.)
# Validate HTML tag sequence
def validate_html_sequence(driver):
    headers = ["h1", "h2", "h3", "h4", "h5", "h6"]
    sequence = []
    for tag in headers:
        elements = driver.find_elements(By.TAG_NAME, tag)
        sequence.append(len(elements))
    return "Pass" if all(count > 0 for count in sequence) else "Fail"

# Validate image alt attributes
def validate_image_alt(driver):
    images = driver.find_elements(By.TAG_NAME, "img")
    missing_alt = [img for img in images if not img.get_attribute("alt")]
    return "Fail" if missing_alt else "Pass"

# Validate URL status codes
def validate_url_status(driver):
    urls = [a.get_attribute("href") for a in driver.find_elements(By.TAG_NAME, "a") if a.get_attribute("href")]
    broken_urls = []
    for url in urls:
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 404:
                broken_urls.append(url)
        except requests.RequestException:
            broken_urls.append(url)
    return "Fail" if broken_urls else "Pass", broken_urls

# Validate currency filter
def validate_currency_filter(driver):
    try:
        currency_dropdown = Select(driver.find_element(By.ID, "currency-dropdown"))  # Update with the actual element ID
        currency_dropdown.select_by_value("USD")  # Change to desired currency
        time.sleep(2)
        tiles = driver.find_elements(By.CLASS_NAME, "property-tile")  # Update with actual class name
        for tile in tiles:
            if "$" not in tile.text:  # Check for currency symbol
                return "Fail"
        return "Pass"
    except:
        return "Fail"

# Scrape and record script data
def scrape_script_data(driver):
    script_data = {}
    try:
        script = driver.find_element(By.XPATH, "//script[contains(text(), 'siteData')]")  # Update XPath if necessary
        data = script.get_attribute("innerHTML")
        # Extract required fields (mock example, update based on actual script format)
        script_data = {
            "SiteURL": driver.current_url,
            "CampaignID": "12345",  # Extract from script data
            "SiteName": "Alojamiento.io",
            "Browser": "Chrome",
            "CountryCode": "US",
            "IP": "192.168.1.1"  # Replace with actual logic to extract IP
        }
    except:
        pass
    return script_data
