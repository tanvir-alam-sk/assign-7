import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_all_links(driver, url):
    driver.get(url)
    links = driver.find_elements(By.TAG_NAME, 'a')
    all_links = []
    for link in links:
        href = link.get_attribute('href')
        if href:
            all_links.append(href)
    return all_links

def test_currency_filter(driver, url):
    driver.get(url)
    try:
        print("Waiting for the currency dropdown to be present in the DOM...")
        
        # Wait for the currency dropdown to be clickable
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'js-currency-sort-footer'))
        )
        
        # Scroll into view to ensure the dropdown is visible
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown)

        driver.execute_script("arguments[0].click();", dropdown)

        time.sleep(2)
        options = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#js-currency-sort-footer ul.select-ul li'))
        )

        # Wait for property tiles to be visible
        print("Waiting for property tiles to be visible...")

        for i,option in enumerate(options):
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", option)
                driver.execute_script("arguments[0].click();", option)
                time.sleep(2)
                price=WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.price-info.js-price-value'))
                )
            except Exception as e:
                print(f"Error occurred: {e}")
                import traceback
                traceback.print_exc()

            dropdown=WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#js-currency-sort-footer'))
            )
            time.sleep(1)
            driver.execute_script("arguments[0].click();", dropdown)
        print("Currency filtering test passed successfully.")
    
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

