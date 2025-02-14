#!/usr/bin/env python3

"""
Description of the script
"""


import argparse
import logging
import os
import requests
import time
from bs4 import BeautifulSoup
import smtplib


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    filename='/home/corym/stock_bot.log'
)


class Product:
    def __init__(
        self,
        title,
        sku,
        url
    ):
        self.title = title
        self.sku = sku
        self.url = url
        
def send_notification(message_body):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    email = os.environ.get('EMAIL') 
    email_password = os.environ.get('EMAIL_PASSWORD')
    s.login(email, email_password)
    # message to be sent
    # sending the mail
    message_subject = "In Stock item Alert!"
    message = 'Subject: {}\n\n{}'.format(message_subject, message_body)

    s.sendmail(email, email, message)
    # terminating the session
    s.quit()

def checkBestBuy():
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    # Extracting the title of the page
    item_list = [
        Product("5080 nvidia", "6614153", "https://www.bestbuy.com/site/nvidia-geforce-rtx-5080-16gb-gddr7-graphics-card-gun-metal/6614153.p?skuId=6614153"),
        Product("5080 ASUS", "6613335", "https://www.bestbuy.com/site/asus-prime-nvidia-geforce-rtx-5080-16gb-gddr7-pci-express-5-0-graphics-card-black/6613335.p?skuId=6613335"),
        Product("5080 Gigabyte", "6615925", "https://www.bestbuy.com/site/gigabyte-nvidia-geforce-rtx-5080-gaming-oc-16g-gddr7-pci-express-5-0-graphics-card-black/6615925.p?skuId=6615925"),
        Product("5080 MSI", "6615227", "https://www.bestbuy.com/site/msi-nvidia-geforce-rtx-5080-16g-gaming-trio-oc-16gb-gddr7-pci-express-gen-5-graphics-card-black/6615227.p?skuId=6615227"),
        Product("5090 Gigabyte", "6615930", "https://www.bestbuy.com/site/gigabyte-nvidia-geforce-rtx-5090-windforce-oc-32g-gddr7-pci-express-5-0-graphics-card-black/6615930.p?skuId=6615930"),
        Product("5090 nvidia", "6614151", "https://www.bestbuy.com/site/nvidia-geforce-rtx-5090-32gb-gddr7-graphics-card-dark-gun-metal/6614151.p?skuId=6614151"),
        Product("5090 ASUS", "6614119", "https://www.bestbuy.com/site/asus-tuf-gaming-nvidia-geforce-rtx-5090-32gb-gddr7-pci-express-5-0-graphics-card-black/6614119.p?skuId=6614119"),
        # TODO remove, just using these for testing 
        # Product("3060", "6468931", "https://www.bestbuy.com/site/gigabyte-nvidia-geforce-rtx-3060-12gb-gddr6-pci-express-4-0-graphics-card-black/6468931.p?skuId=6468931"),
        # Product("ASUS 3060", "6557544", "https://www.bestbuy.com/site/asus-nvidia-geforce-rtx-3060-dual-overclock-12gb-gddr6-pci-express-4-0-graphics-card-black/6557544.p?skuId=6557544")
    ]
    in_stock_message = ""
    for product in item_list:
        response = requests.get(product.url, headers=headers)
        soup = BeautifulSoup(response.content, "html5lib") # If this line causes an error, run 'pip install html5lib' or install html5lib
        mybuttons = soup.find_all("button", {"data-sku-id": product.sku})
        for button in mybuttons:
            if button['data-button-state'] == "ADD_TO_CART":
                in_stock_message = in_stock_message + f"In stock item {soup.title.text} \n {product.url} \n"
                logging.info(f"In stock item {soup.title.text}")
    
    if in_stock_message:
        logging.info(f"In stock item found, sending notification")
        send_notification(f"In stock item {soup.title.text} \n {product.url}")
        time.sleep(2*60*60) # We have been alerted for an in stock item, sleep for the next hour


def main():
    """Main function of the script."""
    logging.info("Starting app")
    parser = argparse.ArgumentParser(description="Description of the script")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG) # Set the logger's level to INFO
        logging.debug("Log level set to debug")

    # Your script logic here
    check_counter = 0
    while True:
        checkBestBuy()
        time.sleep(5*60)  # Pause for 10 minutes
        check_counter += 1
        if check_counter > 24:
            logging.info(f"No Item Found")
            check_counter = 0

    
if __name__ == "__main__":
    main()