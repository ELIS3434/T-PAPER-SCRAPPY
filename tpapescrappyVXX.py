import json
import time
import re
from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def normalize_price(price_str):
    try:
        # Remove currency symbols and non-numeric characters except dots
        price_str = re.sub(r'[^\d.]', '', price_str)
        # Convert to float for JSON serialization compatibility
        return float(price_str)
    except:
        return 0.0

def scrape_amazon(driver):
    url = "https://www.amazon.com/s?k=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".s-main-slot .s-result-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, "h2 a span").text
            price_whole = item.find_element(By.CSS_SELECTOR, ".a-price-whole").text
            price_fraction = item.find_element(By.CSS_SELECTOR, ".a-price-fraction").text
            price = f"{price_whole}.{price_fraction}"
            link = item.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
            results.append({
                "brand": brand,
                "price": price,
                "normalized_price": normalize_price(price),
                "source": "Amazon",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_ebay(driver):
    url = "https://www.ebay.com/sch/i.html?_nkw=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".s-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".s-item__title").text
            price = item.find_element(By.CSS_SELECTOR, ".s-item__price").text
            link = item.find_element(By.CSS_SELECTOR, ".s-item__link").get_attribute("href")
            results.append({
                "brand": brand,
                "price": price,
                "normalized_price": normalize_price(price),
                "source": "eBay",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_walmart(driver):
    url = "https://www.walmart.com/search?q=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".search-result-gridview-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".product-title-link span").text
            price = item.find_element(By.CSS_SELECTOR, ".price-characteristic").text
            link = item.find_element(By.CSS_SELECTOR, ".product-title-link").get_attribute("href")
            results.append({
                "brand": brand,
                "price": price,
                "normalized_price": normalize_price(price),
                "source": "Walmart",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_alibaba(driver):
    url = "https://www.alibaba.com/trade/search?SearchText=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".J-offer-wrapper")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".elements-title-normal__content").text
            price = item.find_element(By.CSS_SELECTOR, ".elements-offer-price-normal__price").text
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            results.append({
                "brand": brand,
                "price": price,
                "normalized_price": normalize_price(price),
                "source": "Alibaba",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_made_in_china(driver):
    url = "https://www.made-in-china.com/products-search/hot-china-products/Toilet_Paper.html"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".product-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".product-name").text
            price = item.find_element(By.CSS_SELECTOR, ".price").text
            link = item.find_element(By.CSS_SELECTOR, ".product-name a").get_attribute("href")
            results.append({
                "brand": brand,
                "price": price,
                "normalized_price": normalize_price(price),
                "source": "Made-in-China",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_thomasnet(driver):
    url = "https://www.thomasnet.com/nsearch.html?cov=NA&what=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".supplier-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".company-name").text
            link = item.find_element(By.CSS_SELECTOR, ".company-name a").get_attribute("href")
            results.append({
                "brand": brand,
                "price": "Contact for price",
                "normalized_price": 0.0,
                "source": "ThomasNet",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_tissue_world(driver):
    url = "https://www.tissueworld.com/search?q=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".product-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".product-title").text
            link = item.find_element(By.CSS_SELECTOR, ".product-link").get_attribute("href")
            results.append({
                "brand": brand,
                "price": "Contact supplier",
                "normalized_price": 0.0,
                "source": "Tissue World",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_risi_info(driver):
    url = "https://www.risiinfo.com/search?q=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".article-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".article-title").text
            link = item.find_element(By.CSS_SELECTOR, ".article-link").get_attribute("href")
            results.append({
                "brand": brand,
                "price": "Subscription required",
                "normalized_price": 0.0,
                "source": "RISI Info",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_global_sources(driver):
    url = "https://www.globalsources.com/toilet-paper.html"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".product-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".product-title").text
            price = item.find_element(By.CSS_SELECTOR, ".product-price").text
            link = item.find_element(By.CSS_SELECTOR, ".product-link").get_attribute("href")
            results.append({
                "brand": brand,
                "price": price,
                "normalized_price": normalize_price(price),
                "source": "Global Sources",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_trade_india(driver):
    url = "https://www.tradeindia.com/search.html?keyword=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".product-card")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".product-title").text
            price = item.find_element(By.CSS_SELECTOR, ".product-price").text
            link = item.find_element(By.CSS_SELECTOR, ".product-link").get_attribute("href")
            results.append({
                "brand": brand,
                "price": price,
                "normalized_price": normalize_price(price),
                "source": "Trade India",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_good_on_you(driver):
    url = "https://goodonyou.eco/search?q=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".brand-card")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".brand-name").text
            link = item.find_element(By.CSS_SELECTOR, ".brand-link").get_attribute("href")
            results.append({
                "brand": brand,
                "price": "Rating information",
                "normalized_price": 0.0,
                "source": "Good On You",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_environmental_paper(driver):
    url = "https://environmentalpaper.org/search?q=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".article-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".article-title").text
            link = item.find_element(By.CSS_SELECTOR, ".article-link").get_attribute("href")
            results.append({
                "brand": brand,
                "price": "Environmental information",
                "normalized_price": 0.0,
                "source": "Environmental Paper",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_kimberly_clark(driver):
    url = "https://www.kimberly-clark.com/search?q=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".product-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".product-name").text
            link = item.find_element(By.CSS_SELECTOR, ".product-link").get_attribute("href")
            results.append({
                "brand": brand,
                "price": "Contact for price",
                "normalized_price": 0.0,
                "source": "Kimberly-Clark",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_pg(driver):
    url = "https://www.pg.com/search?q=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".product-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".product-title").text
            link = item.find_element(By.CSS_SELECTOR, ".product-link").get_attribute("href")
            results.append({
                "brand": brand,
                "price": "Contact for price",
                "normalized_price": 0.0,
                "source": "P&G",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def scrape_essity(driver):
    url = "https://www.essity.com/search?q=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".product-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".product-name").text
            link = item.find_element(By.CSS_SELECTOR, ".product-link").get_attribute("href")
            results.append({
                "brand": brand,
                "price": "Contact for price",
                "normalized_price": 0.0,
                "source": "Essity",
                "link": link
            })
        except NoSuchElementException:
            continue
    return results

def save_results(data, filename):
    # Sort all results by price (highest to lowest)
    all_items = []
    for site_items in data.values():
        # Create a copy of each item to avoid modifying the original data
        processed_items = []
        for item in site_items:
            processed_item = item.copy()
            # Convert normalized_price to float for JSON serialization
            if isinstance(processed_item['normalized_price'], Decimal):
                processed_item['normalized_price'] = float(processed_item['normalized_price'])
            processed_items.append(processed_item)
        all_items.extend(processed_items)
    
    sorted_items = sorted(all_items, key=lambda x: x['normalized_price'], reverse=True)
    
    # Save as JSON with sorted items
    with open(f"{filename}.json", "w", encoding="utf-8") as json_file:
        json.dump({
            "sorted_by_price": sorted_items,
            "by_source": data
        }, json_file, ensure_ascii=False, indent=4)
    
    # Save as TXT with sorted items and by source
    with open(f"{filename}.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write("ALL ITEMS SORTED BY PRICE (HIGHEST FIRST):\n")
        txt_file.write("-" * 50 + "\n\n")
        
        for item in sorted_items:
            txt_file.write(f"Source: {item['source']}\n")
            txt_file.write(f"Brand: {item['brand']}\n")
            txt_file.write(f"Price: {item['price']}\n")
            txt_file.write(f"Link: {item['link']}\n")
            txt_file.write("-" * 30 + "\n")
        
        txt_file.write("\n\nRESULTS BY SOURCE:\n")
        txt_file.write("-" * 50 + "\n\n")
        
        for site, items in data.items():
            txt_file.write(f"{site.upper()}:\n")
            site_items = sorted(items, key=lambda x: x['normalized_price'], reverse=True)
            for item in site_items:
                txt_file.write(f"Brand: {item['brand']}\n")
                txt_file.write(f"Price: {item['price']}\n")
                txt_file.write(f"Link: {item['link']}\n")
                txt_file.write("-" * 30 + "\n")
            txt_file.write("\n")

def main():
    driver = initialize_driver()
    try:
        all_results = {}
        
        print("Scraping Amazon...")
        all_results["Amazon"] = scrape_amazon(driver)
        
        print("Scraping eBay...")
        all_results["eBay"] = scrape_ebay(driver)
        
        print("Scraping Walmart...")
        all_results["Walmart"] = scrape_walmart(driver)
        
        print("Scraping Alibaba...")
        all_results["Alibaba"] = scrape_alibaba(driver)
        
        print("Scraping Made-in-China...")
        all_results["Made-in-China"] = scrape_made_in_china(driver)
        
        print("Scraping ThomasNet...")
        all_results["ThomasNet"] = scrape_thomasnet(driver)
        
        print("Scraping Tissue World...")
        all_results["Tissue World"] = scrape_tissue_world(driver)
        
        print("Scraping RISI Info...")
        all_results["RISI Info"] = scrape_risi_info(driver)
        
        print("Scraping Global Sources...")
        all_results["Global Sources"] = scrape_global_sources(driver)
        
        print("Scraping Trade India...")
        all_results["Trade India"] = scrape_trade_india(driver)
        
        print("Scraping Good On You...")
        all_results["Good On You"] = scrape_good_on_you(driver)
        
        print("Scraping Environmental Paper...")
        all_results["Environmental Paper"] = scrape_environmental_paper(driver)
        
        print("Scraping Kimberly-Clark...")
        all_results["Kimberly-Clark"] = scrape_kimberly_clark(driver)
        
        print("Scraping P&G...")
        all_results["P&G"] = scrape_pg(driver)
        
        print("Scraping Essity...")
        all_results["Essity"] = scrape_essity(driver)
        
        # Save results
        save_results(all_results, "toilet_paper_data")
        print("Results saved to toilet_paper_data.json and toilet_paper_data.txt")
        print("Results are sorted by price (highest first) in both files")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
