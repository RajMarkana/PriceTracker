import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
from utils import scrape_price
from dotenv import load_dotenv

load_dotenv()


def send_email_alert(product, price, config, is_initial=False):
    if not config["email"]["enabled"]:
        return
    sender = os.getenv("EMAIL_ID")
    recipients = config["email"]["recipients"]
    password = os.getenv("EMAIL_PASSWORD")
    if not password:
        logging.error("Missing EMAIL_PASSWORD in .env")
        return

    subject = (
        f"Price Alert: {product['name']}"
        if not is_initial
        else f"Tracking Started: {product['name']}"
    )
    body = f"""
<html>
<head>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: #f5f7fa;
        margin: 0;
        padding: 20px;
    }}
    
    .container {{
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
        max-width: 600px;
        margin: auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }}
    
    .header {{
        text-align: center;
        margin-bottom: 30px;
    }}
    
    .icon {{
        font-size: 48px;
        margin-bottom: 15px;
    }}
    
    h2 {{
        color: #1a202c;
        font-size: 24px;
        margin: 0 0 10px 0;
        font-weight: 600;
    }}
    
    .greeting {{
        font-size: 16px;
        color: #718096;
        margin-bottom: 30px;
    }}
    
    .product-info {{
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 25px;
        margin-bottom: 25px;
    }}
    
    .product-name {{
        font-size: 18px;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 20px;
    }}
    
    .price-row {{
        display: flex-column;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid #e2e8f0;
    }}
    
    .price-row:last-child {{
        border-bottom: none;
    }}
    
    .price-label {{
        color: #718096;
        font-size: 14px;
    }}
    
    .price-value {{
        font-size: 20px;
        font-weight: 600;
        color: #2d3748;
    }}
    
    .current-price {{
        color: #059669;
    }}
    
    .target-price {{
        color: #6366f1;
    }}
    
    .status-message {{
        text-align: center;
        padding: 12px 20px;
        border-radius: 8px;
        margin: 20px 0;
        font-weight: 500;
    }}
    
    .status-below {{
        background-color: #d1fae5;
        color: #065f46;
    }}
    
    .status-tracking {{
        background-color: #e0e7ff;
        color: #3730a3;
    }}
    
    .savings-message {{
        background-color: #fef3c7;
        color: #92400e;
        padding: 12px 20px;
        border-radius: 8px;
        text-align: center;
        margin: 15px 0;
        font-weight: 500;
    }}
    
    a{{
        color: #ffffff;
        display: block;
        padding: 12px 20px;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        text-align: center;
        transition: all 0.2s ease;
        margin-top: 25px;
        color: #ffffff;
        background-color: #4f46e5;
    }}
    .button-text {{
        color: #ffffff;
        text-decoration: none;
    }}

    
    .footer {{
        text-align: center;
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
        color: #718096;
        font-size: 14px;
    }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="icon">{'💰' if not is_initial else '📊'}</div>
        <h2>{'Price Drop Alert' if not is_initial else 'Tracking Started'}</h2>
    </div>
    
    <p class="greeting">Hello! Here's your price update:</p>
    
    <div class="product-info">
        <div class="product-name">{product['name']}</div>
        
        <div class="price-row">
            <span class="price-label">Current Price</span><br/>
            <span class="price-value current-price">₹{price:.2f}</span>
        </div>
        
        <div class="price-row">
            <span class="price-label">Target Price</span><br/>
            <span class="price-value target-price">₹{product['threshold']:.2f}</span>
        </div>
    </div>
    
    {'<div class="status-message status-below">✅ Price is below your target!</div>' if price <= product['threshold'] else '<div class="status-message status-tracking">' + ('✓ Now tracking this product' if is_initial else '⏳ Still monitoring for price drops') + '</div>'}
    
    {'<div class="savings-message">You save ₹' + f'{product["threshold"] - price:.2f}' + ' at current price</div>' if price <= product['threshold'] else ''}
    
    <a href="{product['url']}" target="_blank">
        <span class="button-text">{'Buy Now →' if price <= product['threshold'] else 'View Product →'}</span>
    </a>
    
    <div class="footer">
        <p>Price Tracker Bot • Automated Monitoring</p>
    </div>
</div>
</body>
</html>
"""

    msg = MIMEMultipart()
    msg["From"] = f"Price Tracker Bot <{sender}>"
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)


def send_startup_email(config):
    if not config["email"]["enabled"]:
        return
    sender = os.getenv("EMAIL_ID")
    recipients = config["email"]["recipients"]
    password = os.getenv("EMAIL_PASSWORD")
    if not password:
        logging.error("Missing EMAIL_PASSWORD in .env")
        return
    products = config["products"]
    products_html = ""
    for p in products:
        price = scrape_price(p)
        if price is None:
            continue
        status_text = "Below" if price <= p['threshold'] else "Above"
        status_class = "below" if price <= p['threshold'] else "above"
        products_html += f"""
<tr>
    <td>{p['name']}</td>
    <td class="price">₹{price:.2f}</td>
    <td class="price">₹{p['threshold']:.2f}</td>
    <td><span class="status {status_class}">{status_text}</span></td>
    <td><a href="{p['url']}" class="buy-link">Buy Now</a></td>
</tr>"""

        body = f"""
<html>
<head>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: #f5f7fa;
        padding: 20px;
        margin: 0;
    }}
    
    .container {{
        background-color: #ffffff;
        padding: 30px;
        border-radius: 12px;
        max-width: 800px;
        margin: auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }}
    
    h2 {{
        color: #1a202c;
        font-size: 24px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .subtitle {{
        color: #718096;
        margin-bottom: 25px;
        font-size: 16px;
    }}
    
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background: white;
        border-radius: 8px;
        overflow: hidden;
    }}
    
    th {{
        background-color: #4a5568;
        color: white;
        padding: 14px;
        text-align: left;
        font-weight: 500;
        font-size: 14px;
    }}
    
    td {{
        padding: 14px;
        border-bottom: 1px solid #e2e8f0;
        color: #2d3748;
    }}
    
    tr:last-child td {{
        border-bottom: none;
    }}
    
    tr:hover {{
        background-color: #f7fafc;
    }}
    
    .price {{
        font-weight: 600;
        font-family: monospace;
        font-size: 16px;
    }}
    
    .status {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 500;
    }}
    
    .status.below {{
        background-color: #d4edda;
        color: #155724;
    }}
    
    .status.above {{
        background-color: #f8d7da;
        color: #721c24;
    }}
    
    .buy-link {{
        color: #3182ce;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s;
    }}
    
    .buy-link:hover {{
        color: #2c5282;
        text-decoration: underline;
    }}
    
    .footer {{
        text-align: center;
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
        color: #718096;
        font-size: 14px;
    }}
</style>
</head>
<body>
<div class="container">
    <h2>📊 Price Tracker Dashboard</h2>
    <p class="subtitle">Monitoring your products for price drops</p>
    
    <table>
        <tr>
            <th>Product</th>
            <th>Current Price</th>
            <th>Target Price</th>
            <th>Status</th>
            <th>Action</th>
        </tr>
        {products_html}
    </table>
    
    <div class="footer">
        <p>🤖 Price Tracker Bot • Checking prices every hour</p>
    </div>
</div>
</body>
</html>
"""

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = "Price Tracker Started"
    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
