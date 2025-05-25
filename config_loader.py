import json
import os
import csv
import logging

def load_config(config_file):
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        print("-"*20)
        return create_default_config(config_file)

def create_default_config(config_file):
    default = {
        "products": [{
            "name": "Example",
            "url": "https://example.com",
            "selector": ".price",
            "threshold": 100.0
        }],
        "email": {
            "enabled": False,
            "sender": "rajmarkana1324@gmail.com",
            "password": "",
            "recipients": []
        },
        "check_interval": 6,
        "data_file": "price_history.csv"
    }
    with open(config_file, 'w') as f:
        json.dump(default, f, indent=4)
    return default

def initialize_data_file(path):
    if not os.path.exists(path):
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'product_name', 'price', 'url'])
