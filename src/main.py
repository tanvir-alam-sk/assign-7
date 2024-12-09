from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config import TEST_URL, DRIVER_PATH, OUTPUT_FILE
from test_cases import validate_h1_tag, validate_html_sequence, validate_image_alt
from utils import write_to_excel

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    driver_service = Service(DRIVER_PATH)
    return webdriver.Chrome(service=driver_service, options=options)

def main():
    driver = setup_driver()
    driver.get(TEST_URL)
    results = []

    # Run tests
    h1_result = validate_h1_tag(driver)
    results.append({"Test": "H1 Tag Existence", "Result": h1_result})


    # Add more test results...
    write_to_excel(results, OUTPUT_FILE)

    driver.quit()

if __name__ == "__main__":
    main()
