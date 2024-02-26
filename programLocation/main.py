from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import re
import pyshorteners
import pandas
import os

#may want to factor in user's zip code for closer results. may be good to test with vpn, 
#can possibly obfuscate location with website gathered info. proxy?


firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)

#get rid of? probably will take in and output parameters only.
def search(term, website, sorting, review, post_type):
    #print("[1] Ebay\n[2] Craigslist\n[3] Facebook Marketplace\n[4] Search All")
    print(f"term = {term}, website = {website}")
    
    match website:
        case 1:
            ebay(term, sorting, review, post_type)
        case 2:
            craigslist(term)
        case 3:
            pass
        case 4:
            pass


def shorten(url):
    type_tiny = pyshorteners.Shortener()
    short_url = type_tiny.tinyurl.short(url)
    return short_url


def ebay(term, sorting, review, post_type):

    ebay_prices = []
    driver.get("https://www.ebay.com/")
    #print("[1] Best match\n[2] Time: Ending Soonest\n[3] Time: Newly Listed\n[4] Price + Shipping: Lowest First\n[5] Price + Shipping: Highest First\n[6] Distance: Nearest First")
    time.sleep(2)

    # while True:
    #         selector = int(input("Select Sorting Option: "))
    #         if selector in [1,2,3,4,5,6]:
    #             break
    #         else:
    #             print("Incorrect input, please input integers 1 - 6.")

    match sorting:
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

    while True:        
        listing_percent = review
        if listing_percent < 100.1 or listing_percent > 0:
            break
        else:
            print("Incorrect input, please input numbers only 1 - 100.")

    #print("[1] Filter only Auctions\n[2] Filter only Buy it now\n[3] Process both")
    while True:
        #filter = int(input("Filter by Auction or Buy it now?: "))
        if post_type in [1,2,3]:
            break
        else:
            print("Invalid input. Please enter 1, 2 or 3.")    
    
    auction_filter = False
    buy_filter = False

    match post_type:
        case 1:
            auction_filter = True
        case 2:
            buy_filter = True
        case 3:
            pass

    time.sleep(3)

    ul_element = driver.find_element(By.CSS_SELECTOR, '.srp-results')
    list_elements = ul_element.find_elements(By.CSS_SELECTOR, '[id^="item"][data-viewport*="trackableId"]')

    
    for item in list_elements:
        
        link = item.find_element(By.CSS_SELECTOR, 'div > a')
        url = link.get_attribute('href')
        url = shorten(url)
        current_div = item.find_element(By.CSS_SELECTOR, 'div.s-item__details.clearfix')

        #filter reviews
        reviews = current_div.find_element(By.CSS_SELECTOR, '.s-item__seller-info').text
        reviews = re.search(r"\)\s*(\d+)", reviews).group(1)
        reviews = float(reviews)
        if reviews < listing_percent:
            continue
        
        #filter listing type
        if auction_filter == True:
            try:
                current_div.find_element(By.CSS_SELECTOR, '.s-item__bids.s-item__bidCount')
            except:
                continue
        if buy_filter == True:
            try:    
                current_div.find_element(By.CSS_SELECTOR, '.s-item__purchase-options.s-item__purchaseOptions')
            except:
                continue
            
        #listing info processing
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
            time_left = current_div.find_element(By.CSS_SELECTOR, '.s-item__time').text
            time_left = re.sub(r'Time left\n', '', time_left)
            listing['time'] = time_left
        except:
            pass
        ebay_prices.append(listing)
    output_data(ebay_prices, sorting)


def craigslist(term, sorting):
    craigslist_prices = []
    driver.get("https://www.craigslist.org")
    input_element = driver.find_element(By.CSS_SELECTOR, '#leftbar > div.cl-home-search-query.wide > div > input[type=text]')
    input_element.send_keys(term + Keys.RETURN)


#def facebook_marketplace():


def output_data(ebay_prices, sorting):
    print("output data is being accessed")
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M")

    #adjust for different services, obviously
    output_folder = "Output"
    output_file = f"Ebay Prices - {sorting} - {dt_string}"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    dataframe = pandas.DataFrame(ebay_prices)

    # WIP - width of columns in spreadsheet programs is probably a user issue, not our problem.

    #set width of each column to longest item in list
    # dataframe = dataframe.replace({pandas.NA: '', pandas.NaT: ''})
    # max_width = dataframe.applymap(lambda x: len(str(x))).max()
    # for col in dataframe:
    #     dataframe[col] = dataframe[col].apply(lambda x: f"{x: <{max_width[col]}}" if pandas.notna(x) else '')

    dataframe.to_csv(f"{output_folder}/{output_file}.csv",index=False)