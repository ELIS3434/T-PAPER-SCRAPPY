import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Initialize WebDriver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")  # Optional: Run in headless mode
    service = Service("C:/Users/elinh/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Scrape data from Amazon
def scrape_amazon(driver):
    url = "https://www.amazon.com/s?k=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []

    items = driver.find_elements(By.CSS_SELECTOR, ".s-main-slot .s-result-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".a-size-medium").text
            price = item.find_element(By.CSS_SELECTOR, ".a-price-whole").text
            results.append({"website": "Amazon", "brand": brand, "price": f"${price}"})
        except Exception:
            continue
    return results

# Scrape data from Walmart
def scrape_walmart(driver):
    url = "https://www.walmart.com/search/?query=toilet%20paper"
    driver.get(url)
    time.sleep(5)
    results = []

    items = driver.find_elements(By.CSS_SELECTOR, ".search-result-gridview-item")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".product-title-link span").text
            price = item.find_element(By.CSS_SELECTOR, ".price-characteristic").text
            results.append({"website": "Walmart", "brand": brand, "price": f"${price}"})
        except Exception:
            continue
    return results

# Scrape data from Target
def scrape_target(driver):
    url = "https://www.target.com/s?searchTerm=toilet+paper"
    driver.get(url)
    time.sleep(5)
    results = []

    items = driver.find_elements(By.CSS_SELECTOR, ".h-padding-a-tight")
    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, ".styles__StyledTitle-sc-5js3xt-0").text
            price = item.find_element(By.CSS_SELECTOR, ".styles__PriceText-sc-1e1d2vi-0").text
            results.append({"website": "Target", "brand": brand, "price": price})
        except Exception:
            continue
    return results

# Save output to JSON and TXT
def save_data(data, json_file, txt_file):
    # Save as JSON
    with open(json_file, "w") as jf:
        json.dump(data, jf, indent=4)
    
    # Save as TXT
    with open(txt_file, "w") as tf:
        for entry in data:
            tf.write(f"Website: {entry['website']}, Brand: {entry['brand']}, Price: {entry['price']}\n")

# Main execution
if __name__ == "__main__":
    driver = initialize_driver()
    all_data = []

    try:
        # Scrape from multiple websites
        all_data.extend(scrape_amazon(driver))
        all_data.extend(scrape_walmart(driver))
        all_data.extend(scrape_target(driver))

        print(f"Scraped {len(all_data)} items.")

        # Save combined data
        save_data(all_data, "toilet_paper_data.json", "toilet_paper_data.txt")
        print("Data saved successfully!")

    finally:
        driver.quit()
