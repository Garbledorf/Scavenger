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
    prices = []
    ebay(term, prices)
    print(prices)

def ebay(term, prices):
    driver.get("https://www.ebay.com/")
    input_element = driver.find_element(By.ID, "gh-ac")
    input_element.send_keys(term + Keys.RETURN)
    time.sleep(1.5)
    button_element = driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/div[1]/div/div[1]/div[3]/div[1]/div/span/button' )
    button_element.click()
    time.sleep(.5)
    list_element = driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/div[1]/div/div[1]/div[3]/div[1]/div/span/span/ul/li[4]')
    list_element.click()
    time.sleep(.5)

    ul_element = driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul')
    list_items = ul_element.find_elements(By.XPATH, './li')
    count = 1
    for items in list_items:
        count += 1
        price = driver.find_element(By.XPATH, '//*div[1]/span')
        prices.append(price.text)
    return prices
if __name__=="__main__":
    main()
    