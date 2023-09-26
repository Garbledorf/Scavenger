from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import re
import pyshorteners
import pandas
import os


driver = webdriver.Firefox()

def main():
    search()

def search():
    term = str(input("Enter Search Term: "))
    print("[1] Ebay\n[2] Craigslist\n[3] Facebook Marketplace\n[4] Search All")
    selector = int(input("Select what to search first: "))
    match selector:
        case 1:
            ebay(term)
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass

def shorten(url):
    type_tiny = pyshorteners.Shortener()
    short_url = type_tiny.tinyurl.short(url)
    return short_url


def ebay(term):
    ebay_prices = []
    driver.get("https://www.ebay.com/")
    print("[1] Best match\n[2] Time: Ending Soonest\n[3] Time: Newly Listed\n[4] Price + Shipping: Lowest First\n[5] Price + Shipping: Highest First\n[6] Distance: Nearest First")
    time.sleep(2)
    selector = int(input("Select Sorting Option: "))
    match selector:
        case 1:
            href="https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + term + "&_sacat=0&_sop=12"
            sorting = 'Best match'
            driver.get(href)
        case 2:
            href="https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + term + "&_sacat=0&_sop=1"
            sorting = 'Ending Soonest'
            driver.get(href)
        case 3:
            href="https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + term + "&_sacat=0&_sop=10"
            sorting = 'Newly Listed'
            driver.get(href)
        case 4:
            href="https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + term +"&_sacat=0&_sop=15"
            sorting = 'Lowest First'
            driver.get(href)
        case 5:
            href="https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + term + "&_sacat=0&_sop=16"
            sorting = 'Highest First'
            driver.get(href)
        case 6:
            href="https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + term + "&_sacat=0&_sop=7"
            sorting = 'Nearest First'
            driver.get(href)
    time.sleep(3)


    ul_element = driver.find_element(By.CSS_SELECTOR, '.srp-results')
    list_elements = ul_element.find_elements(By.CSS_SELECTOR, '[id^="item"][data-viewport*="trackableId"]')

    for item in list_elements:
        link = item.find_element(By.CSS_SELECTOR, 'div > a')
        url = link.get_attribute('href')
        url = shorten(url)
        current_div = item.find_element(By.CSS_SELECTOR, 'div.s-item__details.clearfix')
        listing = { 'link': url,
                     'price': current_div.find_element(By.CSS_SELECTOR, '.s-item__price').text,
                     'seller': current_div.find_element(By.CSS_SELECTOR, '.s-item__seller-info').text
                  }
        try:
            bids = current_div.find_element(By.CSS_SELECTOR, '.s-item__bids.s-item__bidCount').text
            bids = re.sub((r' ·'),'',bids)
            listing['bids'] = bids
        except:
            pass
        try:
            #doesnt work with newly listed, fix by searching above it.
            time_left = current_div.find_element(By.CSS_SELECTOR, '.s-item__time').text
            time_left = re.sub(r'Time left\n', '', time_left)
            listing['time'] = time_left
        except:
            pass
        ebay_prices.append(listing)
    output_data(ebay_prices, sorting)

#def craigslist():

#def facebook_marketplace():

def output_data(ebay_prices, sorting):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M")

    output_folder = "Output"
    output_file = f"Ebay Prices - {sorting} - {dt_string}"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    dataframe = pandas.DataFrame(ebay_prices)
    dataframe.to_csv(f"{output_folder}/{output_file}.csv",index=False)

if __name__=="__main__":
    main()
