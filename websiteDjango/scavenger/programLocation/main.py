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


def search(term):
    term = str(input("Enter Search Term: "))
    print("[1] Ebay\n[2] Craigslist\n[3] Facebook Marketplace\n[4] Search All")
    selector = int(input("Select what to search first: "))
    match selector:
        case 1:
            ebay(term)
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


def ebay(term):
    ebay_prices = []
    driver.get("https://www.ebay.com/")
    print("[1] Best match\n[2] Time: Ending Soonest\n[3] Time: Newly Listed\n[4] Price + Shipping: Lowest First\n[5] Price + Shipping: Highest First\n[6] Distance: Nearest First")
    time.sleep(2)

    while True:
            try:
                selector = int(input("Select Sorting Option: "))
                if selector in [1,2,3,4,5,6]:
                    break
                else:
                    print("Incorrect input, please input integers 1 - 6.")
            except:
                print("Incorrect input, please input integers 1 - 6.")
    
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

    while True:        
        listing_percent = float(input(f"Set % positive reviews to filter.\nEnter 30 to only search between 30% to 100% listings: "))
        if listing_percent < 100.1 or listing_percent > 0:
            break
        else:
            print("Incorrect input, please input numbers only 1 - 100.")

    print("[1] Filter only Auctions\n[2] Filter only Buy it now\n[3] Process both")
    while True:
        filter = int(input("Filter by Auction or Buy it now?: "))
        if filter in [1,2,3]:
            break
        else:
            print("Invalid input. Please enter 1, 2 or 3.")    
    
    auction_filter = False
    buy_filter = False

    match filter:
        case 1:
            auction_filter = True
        case 2:
            buy_filter = True
        case 3:
            pass
        
    time.sleep(3)   

    ul_element = driver.find_element(By.CSS_SELECTOR, '.srp-results')
    list_elements = ul_element.find_elements(By.CSS_SELECTOR, '[id^="item"][data-viewport*="trackableId"]')

    #Botting is crowding search results, create filter for low review posts
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
    title = 'Ebay Prices'
    output_data(ebay_prices, sorting, title)


def craigslist(term):
    craigslist_prices = []
    driver.get("https://www.craigslist.org")
    time.sleep(1)
    input_element = driver.find_element(By.CSS_SELECTOR, '#leftbar > div.cl-home-search-query.wide > div > input[type=text]')
    time.sleep(.5)
    input_element.send_keys(term + Keys.RETURN)
    time.sleep(2)
    
    #doesnt work yet
    ordered_element = driver.find_element(By.CSS_SELECTOR, '.results.cl-results-page')
    list_elements = ordered_element.find_elements(By.CSS_SELECTOR, 'li')
    
    for item in list_elements:
        link = item.find_element(By.CSS_SELECTOR, 'a')
        url = link.get_attribute('href')
        url = shorten(url)

        listing = {'link' : url,
                   'price' : item.find_element(By.CSS_SELECTOR, 'div > span').text,
                   'location': item.find_element(By.CSS_SELECTOR, 'div > div.meta').text}
        craigslist_prices.append(listing)
    sorting = 'normal'
    title = 'Craigslist Prices'
    output_data(craigslist_prices, sorting, title)

#def facebook_marketplace():


def output_data(price_array, sorting, title):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M")

    output_folder = "Output"
    if sorting != 'normal':
        output_file = f"{title} - {sorting} - {dt_string}"
    else: 
        output_file = f"{title} - {dt_string}"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    dataframe = pandas.DataFrame(price_array)

    # WIP - width may be a problem with local install of excel
    
    #set width of each column to longest item in list
    # dataframe = dataframe.replace({pandas.NA: '', pandas.NaT: ''})
    # max_width = dataframe.applymap(lambda x: len(str(x))).max()
    # for col in dataframe:
    #     dataframe[col] = dataframe[col].apply(lambda x: f"{x: <{max_width[col]}}" if pandas.notna(x) else '')

    dataframe.to_csv(f"{output_folder}/{output_file}.csv",index=False)
    driver.quit()

if __name__ == "__main__":
    main()
