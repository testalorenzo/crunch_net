#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 20:07:52 2021

@author: ltesta
"""
# still to fix account 
# 4jFSr_fPgL*Y9pF

import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import requests
import time 


driver = webdriver.Chrome(ChromeDriverManager().install())

#search_url="https://www.crunchbase.com/discover/funding_rounds/cb41b0c258d529f6047a4ab91f1e3fe7" 
search_url="https://www.crunchbase.com/discover/funding_rounds/bdda600e03323fdf33dace1524eb7319"
#driver.get(search_url)
#content = driver.page_source
#soup = BeautifulSoup(content)

count=0
count2=0
rounds=[]
organisations=[]
funding_type=[]
money_raised=[]
pre_money=[]
date=[]
investors=[]
places=[]
while count2 <=65000:
    while count <1000:
        driver.get(search_url)
        content = driver.page_source
        soup = BeautifulSoup(content)
        for h in soup.findAll('a', attrs={'aria-label':"Next"}):
            a=h.get("href")
        search_url="https://www.crunchbase.com"+a
        lst=[]
        for i in soup.findAll('div', attrs={'class':"flex-no-grow cb-overflow-ellipsis identifier-label"}):
            a=i.text
            #print(a)
            lst.append(a)
        for i,j in enumerate(lst):
            if i%2==0:
                rounds.append(j)
            elif i%2!=0:
                organisations.append(j)
        for i in soup.findAll('span', attrs={'class':"component--field-formatter field-type-enum ng-star-inserted"}):
            a=i.text
            #print(a)
            funding_type.append(a)
        money=[]    
        for i in soup.findAll('span', attrs={'class':"component--field-formatter field-type-money ng-star-inserted"}):
            a=i.text
            #print(a)
            money.append(a)
        for i,j in enumerate(money):
            if i%2==0:
                money_raised.append(j)
            elif i%2!=0:
                pre_money.append(j)
        for i in soup.findAll('span', attrs={'class':"component--field-formatter field-type-date ng-star-inserted"}):
            a=i.text
            #print(a)
            date.append(a)
        inv=[]
        for i in soup.findAll('span', attrs={'class':"component--field-formatter field-type-identifier-multi"}):
            a=i.text
            #print(a)
            inv.append(a)   
        for i,j in enumerate(inv):
            if i%2==0:
                investors.append(j)
            elif i%2!=0:
                places.append(j)   
        #element3 = driver.find_element_by_xpath("/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/discover/page-layout/div/div/div[2]/section[2]/results/div/div/div[1]/div/results-info/h3/a[2]")
        #element3.click()
        #WebDriverWait(driver, 2)
        count+=50
    count=-50
    element = driver.find_element_by_id("mat-radio-6")
    element.click()
    element2=driver.find_element_by_name("announced_on_max")
    element2.send_keys(Keys.COMMAND, 'a')
    element2.send_keys(Keys.BACKSPACE)
    element2.send_keys(date[-1])
    element2.send_keys(Keys.ENTER) 
    time.sleep(10)
    search_url=driver.current_url
    count2+=1000     


"""    
link=[]
for i in soup.findAll('a', attrs={'class':"component--field-formatter field-type-identifier link-accent ng-star-inserted"}):
    a=i.get("href")
    #print(a)
    link.append(a)
links=[]
for i,j in enumerate(link):
    if i%2==0:
        links.append(j)

investors=[]
for search_url in links:
    driver.get("https://www.crunchbase.com"+search_url)
    content = driver.page_source
    soup = BeautifulSoup(content)
    investor=[]
    for i in soup.findAll('div', attrs={'class':"flex-no-grow cb-overflow-ellipsis identifier-label"}):
        a=i.text
        #print(a)
        investor.append(a)
    investors.append(investor)
"""

df3 = pd.DataFrame({'Organisation':organisations, 'Investors':investors, 'Location':places})
df4 = pd.DataFrame({'Money raised':money_raised, 'Pre-money valuation':pre_money})
df2 = pd.DataFrame({'Round':rounds,'Organisation':organisations, 'Funding type':funding_type, 'Money raised':money_raised, "Pre-money valuation":pre_money, 'Date':date, 'Investors':investors, 'Location':places})  
df = pd.DataFrame({'Round':rounds,'Organisation':organisations, 'Funding type':funding_type, 'Money raised':money_raised, "Pre-money valuation":pre_money, 'Date':date, 'Investors':investors, 'Location':places}) 
df_tot=df.append(df2)
df_tot.to_csv("tot1.csv")
df3.to_csv("partial1.csv")
df4.to_csv("partial2.csv")
trial=set(rounds)

df5 = pd.DataFrame({'Funding type':funding_type})
df5.to_csv("partial3.csv")
df6 = pd.DataFrame({'Date':date})
df6.to_csv("partial4.csv")
df7 = pd.DataFrame({'Round':rounds})
df7.to_csv("partial5.csv")
