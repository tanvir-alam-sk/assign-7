from utils.browser import init_browser
from tests.test_scraping import extract_all_links, test_currency_filter
from tests.test_validations import test_h1_tag, test_html_tag_sequence, test_image_alt, test_url_status_code
from utils.data_scraper import scrape_script_data
from utils.excel_writer import save_to_excel

SCRAPE_OUTPUT_FILE = "results/script_data_results.xlsx" 

def run_tests():
    url = "https://www.alojamiento.io"
    browser = init_browser()
    test_results = []
    
    # result = test_h1_tag(browser, url)
    # test_results.append({"page_url": url, "testcase": "H1 Tag Existence", "status": result, "comments": "Missing H1 Tag" if result == "Fail" else ""})

    # result = test_html_tag_sequence(browser, url)
    # test_results.append({"page_url": url, "testcase": "HTML Tag Sequence", "status": result, "comments": "Missing/Out of Order Tags" if result == "Fail" else ""})

    # result = test_image_alt(browser, url)
    # test_results.append({"page_url": url, "testcase": "Image Alt Attribute", "status": result, "comments": "Missing Alt Attribute" if result == "Fail" else ""})

    # links = extract_all_links(browser, url)
    # url_status_results = test_url_status_code(links)
    # test_results.extend(url_status_results)
    
    result = test_currency_filter(browser, url)
    print(result)
    # test_results.append({"page_url": url, "testcase": "Currency Filter", "status": result['status'], "comments": result['comments']})
    # save_to_excel(test_results,[])
    # data = scrape_script_data(browser, url)
    # if data:
    #     save_to_excel(test_results,[data])
    # else:
    #     print("No data to write to Excel")
    
    browser.quit()

if __name__ == "__main__":
    run_tests()
