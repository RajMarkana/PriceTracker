import schedule
import time
import logging
from datetime import datetime
from utils import scrape_price, save_price
from emailer import send_email_alert, send_startup_email
from config_loader import load_config, initialize_data_file

class PriceTracker:
    def __init__(self, config_file='config.json'):
        self.config = load_config(config_file)
        self.data_file = self.config.get('data_file', 'price_history.csv')
        initialize_data_file(self.data_file)
    
    def check_prices(self, is_initial_run=False):
        logging.info("Starting price check...")
        for product in self.config['products']:
            price = scrape_price(product)
            if price is not None:
                save_price(self.data_file, product['name'], price, product['url'])
                if is_initial_run:
                    send_email_alert(product, price, self.config, is_initial=True)
                elif price < product['threshold']:
                    logging.info(f"Price alert: {product['name']} < threshold")
                    send_email_alert(product, price, self.config)
        logging.info("Price check completed.")
    
    def schedule_checks(self):
        interval = self.config.get('check_interval', 1)
        send_startup_email(self.config)
        self.check_prices(is_initial_run=True)
        schedule.every(interval).hours.do(self.check_prices)
        logging.info(f"Scheduled every {interval} hours.")
        while True:
            schedule.run_pending()
            time.sleep(60)
