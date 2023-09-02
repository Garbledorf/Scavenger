from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time


import requests

#implement better, ugly placement
driver = webdriver.Firefox()

def main():
    search()

#create class, group functions, get basic search functionality running
def search():
    print("Enter Search Term: ")
    term = str(input())
    ebay_prices = []
    ebay(term, ebay_prices)
    print(ebay_prices)

def ebay(term, ebay_prices):
    driver.get("https://www.ebay.com/")
    input_element = driver.find_element(By.ID, "gh-ac")
    input_element.send_keys(term + Keys.RETURN)
    time.sleep(3)
    button_element = driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/div[1]/div/div[1]/div[3]/div[1]/div/span/button' )
    button_element.click()
    time.sleep(.5)
    list_element = driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/div[1]/div/div[1]/div[3]/div[1]/div/span/span/ul/li[4]')
    list_element.click()
    time.sleep(.5)

    ul_element = driver.find_element(By.XPATH, "//div[@id='srp-river-results']/ul")
    list_items = ul_element.find_elements(By.XPATH, "//li[@class='s-item s-item__pl-on-bottom']")
    count = 2
    while count < len(list_items):
        for item in list_items:
            count += 1
            single_price = item.find_element(By.XPATH, ".//span[@class='s-item__price']")
            ebay_prices.append(single_price.text)
    return ebay_prices

if __name__=="__main__":
    main()
    