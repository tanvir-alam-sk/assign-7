from selenium.webdriver.common.by import By
import time

def scrape_data(driver, url):
    driver.get(url)
    try:
        script_data = driver.find_element(By.TAG_NAME, 'script').get_attribute('innerHTML')
        return script_data
    except Exception as e:
        return "Fail"

def scrape_script_data(driver, url):
    driver.get(url)
    script_data = driver.execute_script("return window.ScriptData")
    
    if isinstance(script_data, dict):
        site_url = script_data['config'].get('SiteUrl', 'Not Found')
        site_name = script_data['config'].get('SiteName', 'Not Found')
        campaign_id = script_data['pageData'].get('CampaignId', 'Not Found')
        
        user_info = script_data.get('userInfo', {})
        browser = user_info.get('Browser', 'Not Found')
        country_code = user_info.get('CountryCode', 'Not Found')
        ip = user_info.get('IP', 'Not Found')
        
        return {
            "SiteURL": site_url,
            "SiteName": site_name,
            "CampaignID": campaign_id,
            "Browser": browser,
            "CountryCode": country_code,
            "IP": ip,
        }
    return None
