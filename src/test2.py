import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Initialize browser and set options
SCRAPE_OUTPUT_FILE = "script_data_results.xlsx" 
def init_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment for headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Test: H1 Tag Existence
def test_h1_tag(driver, url):
    driver.get(url)
    try:
        h1_tag = driver.find_element(By.TAG_NAME, "h1")
        return "Pass" if h1_tag else "Fail"
    except:
        return "Fail"

# Test: HTML Tag Sequence (H1-H6)
def test_html_tag_sequence(driver, url):
    driver.get(url)
    tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    for i in range(len(tags)-1):
        current_tag = driver.find_elements(By.TAG_NAME, tags[i])
        next_tag = driver.find_elements(By.TAG_NAME, tags[i+1])
        if not current_tag and next_tag:
            return "Fail"
    return "Pass"

# Test: Image Alt Attribute
def test_image_alt(driver, url):
    driver.get(url)
    images = driver.find_elements(By.TAG_NAME, 'img')
    for img in images:
        if not img.get_attribute("alt"):
            return "Fail"
    return "Pass"

# Test: URL Status Code
def test_url_status_code(links):
    status_codes = []
    for link in links:
        try:
            if "https://www.alojamiento.io" in link:
                print(f"Testing page: {link}")
                response = requests.get(link)
                if response.status_code == 404:
                    status_codes.append({"page_url": link, "status": "Fail", "status_code": 404})
                else:
                    status_codes.append({"page_url": link, "status": "Pass", "status_code": response.status_code})
        except requests.RequestException as e:
            status_codes.append({"page_url": link, "status": "Fail", "status_code": str(e)})
    return status_codes

# Test: Extract All Links on the Page
def extract_all_links(driver, url):
    driver.get(url)
    # Extract all anchor tags from the page
    links = driver.find_elements(By.TAG_NAME, 'a')
    all_links = []
    for link in links:
        href = link.get_attribute('href')
        if href:
            all_links.append(href)
    return all_links

# Test: Currency Filter and Property Tile Currency Change
def test_currency_filter(driver, url):
    driver.get(url)
    try:
        # Assuming currency selector is a dropdown with class name 'currency-selector'
        currency_selector = driver.find_element(By.CLASS_NAME, 'price-info')
        currency_selector.click()
        time.sleep(2)  # Wait for dropdown to load
        # Change to a new currency (assuming 'USD' exists in the options)
        currency_selector.find_element(By.XPATH, "//option[@value='USD']").click()
        time.sleep(2)  # Wait for property tiles to update
        
        # Check if the property tile currency is updated (Assuming property tiles have class 'property-tile')
        properties = driver.find_elements(By.CLASS_NAME, 'property-tile')
        for property_tile in properties:
            if "USD" not in property_tile.text:
                return "Fail"
        return "Pass"
    except Exception as e:
        return "Fail"

# Test: Scrape Data from Script and Record
def scrape_data(driver, url):
    driver.get(url)
    try:
        # Example: Extracting data from a <script> tag with JSON data
        script_data = driver.find_element(By.TAG_NAME, 'script').get_attribute('innerHTML')
        return script_data
    except Exception as e:
        return "Fail"

# Save test results to Excel file
def save_to_excel(test_results, filename="test_results.xlsx"):
    df = pd.DataFrame(test_results)
    df.to_excel(filename, index=False)




def scrape_script_data(driver, url):
    # driver = webdriver.Chrome()
    driver.get(url)
    script_data=driver.execute_script("return window.ScriptData")
    pagedata = script_data.get('pagedata', {})
    if isinstance(script_data,dict):
        site_url=script_data['config'].get('SiteUrl', 'Not Found')
        site_name=script_data['config'].get('SiteName', 'Not Found')
        campaing_id=script_data['pageData'].get('CampaignId', 'Not Found')
        
        user_info=script_data.get('userInfo',{})
        browser=user_info.get('Browser','Not Found')
        country_code=user_info.get('CountryCode','Not Found')
        ip=user_info.get('IP','Not Found')
        return {
                        "SiteURL": site_url,
                        "SiteName": site_name,
                        "CampaignID": campaing_id,
                        "Browser": browser,
                        "CountryCode": country_code,
                        "IP": ip,
                    }
    else:
        site_url=site_name,=campaing_id=browser=country_code=ip='Not Found'
        data=[]
        return data
    

def write_to_excel(data, filename):
    try:
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Save to Excel
        df.to_excel(filename, index=False)
        print(f"Data saved successfully to {filename}")
    
    except Exception as e:
        print(f"Error saving to Excel: {e}")


# Main test execution function
def run_tests():
    url = "https://www.alojamiento.io/"  # Test site URL
    browser = init_browser()

    test_results = []
    
    # Test 1: H1 Tag Existence
    result = test_h1_tag(browser, url)
    test_results.append({"page_url": url, "testcase": "H1 Tag Existence", "status": result, "comments": "Missing H1 Tag" if result == "Fail" else ""})

    # Test 2: HTML Tag Sequence (H1-H6)
    result = test_html_tag_sequence(browser, url)
    test_results.append({"page_url": url, "testcase": "HTML Tag Sequence", "status": result, "comments": "Missing/Out of Order Tags" if result == "Fail" else ""})

    # Test 3: Image Alt Attribute
    result = test_image_alt(browser, url)
    test_results.append({"page_url": url, "testcase": "Image Alt Attribute", "status": result, "comments": "Missing Alt Attribute" if result == "Fail" else ""})

    # Test 4: Extract All Links on the Page
    links = extract_all_links(browser, url)
    print(f"Extracted {len(links)} links from the landing page.")
    
    # Test 5: URL Status Code (Test all extracted links)
    url_status_results = test_url_status_code(links)
    test_results.extend(url_status_results)
    
    # Test 6: Currency Filter
    result = test_currency_filter(browser, url)
    test_results.append({"page_url": url, "testcase": "Currency Filter", "status": result, "comments": "Currency Not Updated" if result == "Fail" else ""})

    # Test 7: Scrape Data
    data = scrape_data(browser, url)
    test_results.append({"page_url": url, "testcase": "Scrape Data", "status": "Pass" if data != "Fail" else "Fail", "comments": "Data not found" if data == "Fail" else ""})

    # Save results to Excel
    save_to_excel(test_results)

    data = []

    script_data = scrape_script_data(browser, url)
    if script_data:
        data.append(script_data)
    else:
        print("No valid script data found")
    print(data)
    if data:
        write_to_excel(data, SCRAPE_OUTPUT_FILE)
    else:
        print("No data to write to Excel")
    
    # Close the browser
    browser.quit()

# Run the tests
if __name__ == "__main__":
    run_tests()


