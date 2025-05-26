
# PriceTracker📈

A Python-based price tracking tool that monitors prices of products and sends alerts when prices drop below a certain threshold.

## Table of Contents

* [Introduction](#introduction)
* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Configuration](#configuration)
* [Contributing](#contributing)
* [License](#license)

## Introduction

PriceTracker is a simple tool that helps you keep track of prices of products you're interested in. It uses a configuration file to store product information and sends email alerts when prices drop below a certain threshold.

## Features

* Monitor prices of multiple products
* Send email alerts when prices drop below a certain threshold
* Store price history in a CSV file
* Configure product information and alert thresholds using a JSON configuration file
* AI-Powered Summary Generation: Utilize the Google Gemini model to generate high-quality summaries of product price alerts

## Installation

To install PriceTracker, follow these steps:

1. Clone the repository: `git clone https://github.com/RajMarkana/PriceTracker.git`
2. Install dependencies using UV: `uv install`
3. Create a configuration file: `config.json` (see [Configuration](#configuration) for details)
4. Create a `.env` file with your email credentials:
```bash
EMAIL_ID=your-email@example.com
EMAIL_PASSWORD=your-email-app-password
GOOGLE_API_KEY=your-gemini-api-key
```

## Usage

1. Run the tracker: `uv run main.py`
2. The tracker will monitor prices and send email alerts as configured

## Configuration

The configuration file `config.json` should contain the following information:

* `products`: a list of product objects with the following properties:
	+ `name`: product name
	+ `url`: product URL
    + `selector`: Price Selector (Find Using Inspect Element)
	+ `threshold`: price threshold for alerts
* `data_file`: path to the CSV file for storing price history
* `email`: email configuration for sending alerts

Example `config.json` file:
```json
{
    "products": [
        {
            "name": "Product 1",
            "url": "https://example.com/product1",
            "selector": ".price ",
            "threshold": 10.99
        },
        {
            "name": "Product 2",
            "url": "https://example.com/product2",
            "selector": ".price ",
            "threshold": 5.99
        }

    ],
    "email": {
        "enabled": true,
        "recipients": ["sample@example.com"]
    },
    "check_interval": 1,
    "data_file": "price_history.csv"
}
```
## Contributing

Contributions are welcome! To contribute, please:

1. Fork the repository
2. Create a new branch: `git checkout -b your-branch-name`
3. Make changes and commit: `git commit -m "your-commit-message"`
4. Push changes: `git push origin your-branch-name`
5. Open a pull request

## License

This project is licensed under the MIT License.
