import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import logging

def scrape_price(product):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.google.com/",
        }

        response = requests.get(product['url'], headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.select_one(product['selector'])
        if not element:
            logging.error(f"Selector failed for {product['name']}")
            return None
        price_text = element.text.strip()
        price = float(''.join(c for c in price_text if c.isdigit() or c == '.'))
        return price
    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        return None

def save_price(file_path, name, price, url):
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), name, price, url])
