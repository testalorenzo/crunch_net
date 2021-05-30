# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:05:27 2021

@author: Marco
"""

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
search_url="https://www.crunchbase.com/search/principal.investors/c12768e59b63a9f89406a625d393b233"
#driver.get(search_url)
#content = driver.page_source
#soup = BeautifulSoup(content)

count=0
count2=0
investor_company=[]
investor_location=[]
investor_type=[]
investor_patentsGranted=[]
investor_trademarks=[]
investor_founded = []
investor_industries = []
investor_investments = []
investor_rank = []
investors=[]
places=[]
while count2 <= 5000:
    while count <1000:
        driver.get(search_url)
        content = driver.page_source
        soup = BeautifulSoup(content)
        for h in soup.findAll('a', attrs={'aria-label':"Next"}):
            a=h.get("href")
        search_url="https://www.crunchbase.com"+a
        tot=[]
        for i in soup.findAll('field-formatter', attrs={'class':"cb-margin-medium-horizontal"}):
            a=i.text
            #print(a)
            tot.append(a)
        for i,j in enumerate(tot):
            if i%9==0:
                investor_company.append(j)
            if i%9==1:
                investor_location.append(j)
            if i%9==2:
                investor_type.append(j)
            if i%9==3:
                investor_patentsGranted.append(j)
            if i%9==4:
                investor_trademarks.append(j)
            if i%9==5:
                investor_founded.append(j)
            if i%9==6:
                investor_industries.append(j)
            if i%9==7:
                investor_investments.append(j)
            elif i%9==8:
                investor_rank.append(j)
                
        #element3 = driver.find_element_by_xpath("/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/discover/page-layout/div/div/div[2]/section[2]/results/div/div/div[1]/div/results-info/h3/a[2]")
        #element3.click()
        #WebDriverWait(driver, 2)
        count+=50
    count= 0
    element = driver.find_element_by_id("mat-input-2")
    element.click()
    element.send_keys(Keys.CONTROL, 'a')
    element.send_keys(Keys.BACKSPACE)
    element.send_keys(investor_rank[-1])
    element.send_keys(Keys.ENTER) 
    time.sleep(10)
    search_url=driver.current_url
    count2+=1000     

df_investors1 = pd.DataFrame({'investor_company':investor_company, 
                             'investor_location':investor_location,
                             'investor_type':investor_type,
                             'investor_patentsGranted':investor_patentsGranted,
                             'investor_trademarks':investor_trademarks,
                             'investor_founded':investor_founded,
                             'investor_industries':investor_industries,
                             'investor_investments':investor_investments,
                             'investor_rank':investor_rank})
df_investors = pd.DataFrame({'investor_company':investor_company, 
                             'investor_location':investor_location,
                             'investor_type':investor_type,
                             'investor_patentsGranted':investor_patentsGranted,
                             'investor_trademarks':investor_trademarks,
                             'investor_founded':investor_founded,
                             'investor_industries':investor_industries,
                             'investor_investments':investor_investments,
                             'investor_rank':investor_rank})
df_investors_2 = df_investors.drop_duplicates()
df_investors_2 = df_investors_2.assign(investor_company = df_investors_2.investor_company.str.lstrip())
investors_org = pd.Series(df_tot_11.Investors).unique()
df_investors_2.investor_company
df_investors_2.to_csv("df_investors.csv")



