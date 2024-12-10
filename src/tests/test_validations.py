from selenium.webdriver.common.by import By
import requests

def test_h1_tag(driver, url):
    driver.get(url)
    try:
        h1_tag = driver.find_element(By.TAG_NAME, "h1")
        return "Pass" if h1_tag else "Fail"
    except:
        return "Fail"

def test_html_tag_sequence(driver, url):
    driver.get(url)
    tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    for i in range(len(tags)-1):
        current_tag = driver.find_elements(By.TAG_NAME, tags[i])
        next_tag = driver.find_elements(By.TAG_NAME, tags[i+1])
        if not current_tag and next_tag:
            return "Fail"
    return "Pass"

def test_image_alt(driver, url):
    driver.get(url)
    images = driver.find_elements(By.TAG_NAME, 'img')
    for img in images:
        if not img.get_attribute("alt"):
            return "Fail"
    return "Pass"

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
