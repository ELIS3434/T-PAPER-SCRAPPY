import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Initialize WebDriver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")  # Optional: Run without UI for efficiency
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Scraping functions for each site
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
            results.append({"brand": brand, "price": price})
        except:
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
            results.append({"brand": brand, "price": price})
        except:
            continue
    return results

def scrape_made_in_china(driver):
    url = "https://www.made-in-china.com/products-search/hot-china-products/Toilet_Paper.html"
    driver.get(url)
    time.sleep(5)
    results = []
    items = driver.find_elements(By.CSS_SELECTOR, ".product-container")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".product-title").text
            price = item.find_element(By.CSS_SELECTOR, ".product-price").text
            results.append({"brand": brand, "price": price})
        except:
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
            results.append({"brand": brand, "price": price})
        except:
            continue
    return results

# For sites with mostly textual or informational content, scraping brands or prices is not applicable. Here's how to handle those:
def scrape_info_sites(driver, url):
    driver.get(url)
    time.sleep(5)
    page_title = driver.title
    return [{"info": f"Scraped content from {page_title}"}]

# Save results to JSON and TXT files
def save_results(data, filename):
    # Save as JSON
    with open(f"{filename}.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    # Save as TXT with headers for each site
    with open(f"{filename}.txt", "w", encoding="utf-8") as txt_file:
        for site, items in data.items():
            txt_file.write(f"{site.upper()}:\n")
            for item in items:
                txt_file.write(f"{item}\n")
            txt_file.write("\n")  # Add space between sites

# Main function
def main():
    driver = initialize_driver()
    try:
        # Add each site to scrape
        all_results = {}

        print("Scraping Amazon...")
        all_results["Amazon"] = scrape_amazon(driver)

        print("Scraping Alibaba...")
        all_results["Alibaba"] = scrape_alibaba(driver)

        print("Scraping Made-in-China...")
        all_results["MadeInChina"] = scrape_made_in_china(driver)

        print("Scraping Walmart...")
        all_results["Walmart"] = scrape_walmart(driver)

        # Informational sites
        info_sites = [
            "https://www.thomasnet.com",
            "https://www.tissueworld.com",
            "https://www.risiinfo.com",
            "https://goodonyou.eco",
            "https://environmentalpaper.org",
            "https://www.kimberly-clark.com",
            "https://www.pg.com",
            "https://www.essity.com",
        ]
        for site in info_sites:
            print(f"Scraping {site}...")
            all_results[site] = scrape_info_sites(driver, site)

        # Save results
        save_results(all_results, "toilet_paper_data")
        print("Results saved to toilet_paper_data.json and toilet_paper_data.txt")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
