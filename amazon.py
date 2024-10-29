
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import asyncio
import json
import csv


class AmazonScraper:
    def __init__(self, url, proxy=None):
        self.url = url
        self.proxy = proxy
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def scrape_product(self):
        try:
            response = requests.get(self.url, proxies=self.proxy)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            product_name = soup.find('span', {'id': 'productTitle'}).text.strip()
            price = soup.find('span', {'id': 'priceblock_ourprice'}).text.strip()
            rating = soup.find('span', {'id': 'acrPopover'}).text.strip()
            reviews = soup.find('span', {'id': 'acrCustomerReviewText'}).text.strip()
            availability = soup.find('div', {'id': 'availability'}).text.strip()
            data = {
                'Product Name': product_name,
                'Price': price,
                'Rating': rating,
                'Reviews': reviews,
                'Availability': availability
            }
            return data
        except Exception as e:
            print(f"Error scraping product: {e}")
            return None

    def scrape_product_selenium(self):
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'productTitle')))
            product_name = self.driver.find_element_by_id('productTitle').text
            price = self.driver.find_element_by_id('priceblock_ourprice').text
            rating = self.driver.find_element_by_id('acrPopover').text
            reviews = self.driver.find_element_by_id('acrCustomerReviewText').text
            availability = self.driver.find_element_by_id('availability').text
            data = {
                'Product Name': product_name,
                'Price': price,
                'Rating': rating,
                'Reviews': reviews,
                'Availability': availability
            }
            return data
Exception as e:
            print(f"Error scraping product using Selenium: {e}")
            return None

    def save_to_csv(self, data, filename='amazon_products.csv'):
        try:
            df = pd.DataFrame([data])
            if not pd.read_csv(filename).empty:
                df.to_csv(filename, mode='a', header=False, index=False)
            else:
                df.to_csv(filename, mode='w', header=True, index=False)
        except Exception as e:
            print(f"Error saving to CSV: {e}")

    def save_to_json(self, data, filename='amazon_products.json'):
        try:
            with open(filename, 'ab') as f:
                json.dump(data, f)
                f.write('\n'.encode())
        except Exception as e:
            print(f"Error saving to JSON: {e}")


class ProxyMiddleware:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
        self.current_proxy = 0

    def get_proxy(self):
        return self.proxy_list[self.current_proxy]

    def rotate_proxy(self):
        self.current_proxy = (self.current_proxy + 1) % len(self.proxy_list)


def scrape_product(url, scraper):
    data = scraper.scrape_product()
    if data:
        scraper.save_to_csv(data)
        scraper.save_to_json(data)
        print(data)


def main():
    url = 'https://www.amazon.com/dp/B076MX9VG9'
    proxy_list = ['http://proxy1:8080', 'http://proxy2:8080']
    proxy_middleware = ProxyMiddleware(proxy_list)
    proxy = {'http': proxy_middleware.get_proxy(), 'https': proxy_middleware.get_proxy()}
    scraper = AmazonScraper(url, proxy)

    # Scrape product data using requests
    data = scraper.scrape_product()
    if data:
        scraper.save_to_csv(data)
        scraper.save_to_json(data)
        print(data)

    # Scrape product data using Selenium
    data_selenium = scraper.scrape_product_selenium()
    if data_selenium:
        scraper.save_to_csv(data_selenium)
        scraper.save_to_json(data_selenium)
        print(data_selenium)


if __name__ == "__main__":
    main()
