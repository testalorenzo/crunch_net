# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 08:50:18 2021

@author: Marco
"""

import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.common.keys import Keys
import datetime
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import urllib
import geopy
from geopy.geocoders import Nominatim
import os

#READING
df1 = pd.read_csv("C:/Users/Marco/Documents/GitHub/crunch_net/partial1.csv") 
df2 = pd.read_csv("C:/Users/Marco/Documents/GitHub/crunch_net/partial2.csv") 
df3 = pd.read_csv("C:/Users/Marco/Documents/GitHub/crunch_net/partial3.csv") 
df4 = pd.read_csv("C:/Users/Marco/Documents/GitHub/crunch_net/partial4.csv") 
df5 = pd.read_csv("C:/Users/Marco/Documents/GitHub/crunch_net/partial5.csv") 
df_tot1 = pd.read_csv("C:/Users/Marco/Documents/GitHub/crunch_net/tot1.csv")

#CUT
df1_1 = df1.truncate(after = 28408)
df2_1 = df2.truncate(after = 28408)
df3_1 = df3.truncate(after = 28408)
df4_1 = df4.truncate(after = 28408)
df5_1 = df5.truncate(after = 28408)

#UNITE
df_tot2 = pd.concat([df1_1, df2_1, df3_1, df4_1, df5_1], axis = 1).T.drop_duplicates().T
df_tot = df_tot1.append(df_tot2)

print(df_tot.columns.tolist())

#DELETE ROUND (REDUNDANCE) AND UNNAMED
df_tot_1 = df_tot.drop(['Unnamed: 0', 'Round'], axis = 1)
df_tot_1.index = range(len(df_tot_1))           

#DELETE DUPLICATES
df_tot_2 = df_tot_1.drop_duplicates()
df_tot_2.index = range(len(df_tot_2))
df_tot_2.dtypes

#CONVERT TO DATETIME
df_tot_2['Date'] = pd.to_datetime(df_tot_2['Date'])

#INDEXIAMO
df_tot_2['Index'] = range(len(df_tot_2))
df_tot_2.to_csv('tot_unexploded.csv')
#SPLITTIAMOINVESTORS
df_tot_3 = df_tot_2.assign(Investors=df_tot_2.Investors.str.split(", ")).explode('Investors')
df_tot_4 = df_tot_3
df_tot_4["Investors"].replace({" — ": "Missing"}, inplace=True)

#TOLGO PRIMO WHITESPACE
df_tot_5 = df_tot_4.assign(Organisation = df_tot_4.Organisation.str.lstrip())
df_tot_6 = df_tot_5.assign(Investors = df_tot_5.Investors.str.lstrip())
df_tot_7 = df_tot_6.assign(Location = df_tot_6.Location.str.lstrip())

#GEOGRAPHICAL
df_tot_8 = df_tot_7.assign(Loc_Org = df_tot_7.Location.str.split(", "))
df_tot_8.index = range(len(df_tot_8))
loc_org_1 = [] 
for x in range(len(df_tot_8.Loc_Org)):
    if len(df_tot_8.Loc_Org[x]) ==4:
        loc_org_1.append(df_tot_8.Loc_Org[x][0])
    else:
        loc_org_1.append('Missing')
loc_org_city = pd.Series(loc_org_1)
loc_org_2 = []
for x in range(len(df_tot_8.Loc_Org)):
    if len(df_tot_8.Loc_Org[x]) ==4:
        loc_org_2.append(df_tot_8.Loc_Org[x][1])
    else:
        loc_org_2.append('Missing')
loc_org_region = pd.Series(loc_org_2)
loc_org_3 = []
for x in range(len(df_tot_8.Loc_Org)):
    if len(df_tot_8.Loc_Org[x]) ==4:
        loc_org_3.append(df_tot_8.Loc_Org[x][2])
    else:
        loc_org_3.append('Missing')
loc_org_country = pd.Series(loc_org_3)
loc_org_4 = []
for x in range(len(df_tot_8.Loc_Org)):
    if len(df_tot_8.Loc_Org[x]) ==4:
        loc_org_4.append(df_tot_8.Loc_Org[x][3])
    else:
        loc_org_4.append('Missing')
loc_org_continent = pd.Series(loc_org_4)
geolocator = Nominatim(user_agent = "generone")
df_tot_9 = df_tot_8.assign(geo_org = loc_org_city.str.cat(loc_org_country, sep = ", "))
df_tot_9 = df_tot_9.assign(loc_org_city = loc_org_city).assign(loc_org_region = loc_org_region).assign(loc_org_country = loc_org_country).assign(loc_org_continent = loc_org_continent)
cities = pd.Series(df_tot_9.geo_org).unique()
cities[955] = 'Bundang-dong, South Korea'
cities[1163] = 'Saint Patrick, Trinidad and Tobago'
cities[1189] = 'Dalavich, United Kingdom'
cities[1489] = 'Brehan, France'
cities[1518] = 'Fratticiola selvatica, Italy'
cities[1532] = 'Funabashi, Japan'
cities[1615] = 'Nanshan, China'
cities[2153] = 'Dee why, Australia'
cities[2159] = 'Changsha Hsien, China'
cities[2262] = 'Alaska Peninsula National Wildlife Refuge, United States'
cities[2584] = 'WaKeeney, United States'
cities[2616] = 'Wollongong, Australia'
cities[2724] = 'Ometz, Israel'
cities[2793] = 'Kortedala, Sweden'
cities[2832] = 'Kanagawa, Japan'
cities[2840] = 'Ness Ziona, Israel'
cities[3048] = 'Reggio Emilia, Italy'
cities[3120] = 'Batzra, Israel'
cities[3215] = 'Gilmanton, United States'
cities[3266] = 'Ivanovo, Russian Federation'
cities[3413] = 'McCordsville, United States'
cities[3440] = 'Mokapu, United States'
cities[3498] = 'Kiryat Ono, Israel'
cities[3528] = 'Milton Bryan, United Kingdom'
coo_org = [0]*len(cities) 
for x in range(3528, len(cities)):
    if cities[x] != 'Missing, Missing':
        data = geolocator.geocode(cities[x])
        coo_org[x]=tuple((data.point.latitude, data.point.longitude))
        print(x)
    else:
        coo_org[x] = 'Missing'
coo_org = pd.Series(coo_org)
coo_org_city = coo_org[0:-1]
cities_new= cities
cities_old = pd.Series(df_tot_9.geo_org).unique()
df_cities = pd.DataFrame({'geo_org': cities_old, 'coo_org':coo_org_city})
df_tot_10 = pd.merge(df_tot_9, df_cities)
df_tot_10.to_csv("tot2.csv")
df_tot_11 = df_tot_10
df_tot_11.to_csv("tot3.csv")


countries_org = pd.Series(df_tot_11.loc_org_country).unique()
countries_org[77]='Palestine'
coo_org_country = [0]*len(countries_org) 
for x in range(75,len(coo_org_country)):
    if coo_org_country[x] != 'Missing':
        data = geolocator.geocode(countries_org[x])
        coo_org_country[x]=tuple((data.point.latitude, data.point.longitude))
        print(x)
    else:
        coo_org_country[x] = 'Missing'
coo_org_country = pd.Series(coo_org_country)
countries_old = pd.Series(df_tot_11.loc_org_country).unique()
df_countries = pd.DataFrame({'loc_org_country': countries_old, 'coo_org_country': coo_org_country})
df_tot_12 = pd.merge(df_tot_11, df_countries)

regions_org = pd.Series(df_tot_12.loc_org_region).unique()
regions_org[0] = 'Seoul'
regions_org[1] = 'Chungcheongbuk-do'
regions_org[3] = 'Incheon'
regions_org[4] = 'Daejeon'
regions_org[5] = 'Chungcheongnam-do'
regions_org[6] = 'Daegu'
regions_org[7] = 'Busan'
regions_org[9] = 'Gwangju'
regions_org[274] = 'Perm Krai'
regions_org[592] = 'Reykjavík'
regions_org[593] = 'Ísafjörður'
regions_org[594] = 'Akureyri'
regions_org[595] = 'Vestmannaeyjar'
regions_org[596] = 'Siglufjörður'
regions_org[597] = 'Grenivík'
regions_org[598] = 'Mosfell'
regions_org[632] = 'Ljubljana'
regions_org[633] = 'Trbovlje'
regions_org[634] = 'Maribor'
regions_org[671] = 'Rhodope'
regions_org[681] = 'Greenland'


coo_org_region = [0]*len(regions_org) 
for x in range(670,len(coo_org_region)):
    if coo_org_region[x] != 'Missing':
        data = geolocator.geocode(regions_org[x])
        coo_org_region[x]=tuple((data.point.latitude, data.point.longitude))
        print(x)
    else:
        coo_org_region[x] = 'Missing'
coo_org_region = pd.Series(coo_org_region)
regions_old = pd.Series(df_tot_12.loc_org_region).unique()
df_regions= pd.DataFrame({'loc_org_region': regions_old, 'coo_org_region': coo_org_region})
df_tot_13 = pd.merge(df_tot_12, df_regions)
df_tot_13.to_csv('tot_coo_org.csv')



#PLOTTINO
regions_org[681]
datino = geolocator.geocode('Reykjavík')
datino.point.longitude

s = df_tot_2['Date'].value_counts().sort_index()
s2 = pd.DatetimeIndex(df_tot_2['Date']).year.value_counts().sort_index()
s.plot()
s2
s2.plot()
pippo = df_tot_2.assign(Investors=df_tot_2.Investors.str.split(",")).explode('Investors')
df_tot_2 = df_tot_2.drop(['investors2'], axis = 1)
investors3
pippo = df_tot_3['Investors'].value_counts().sort_index()
pippo[pippo>1000].plot()
df_tot_4.dtypes
set(df_tot_9.geo_org)
cities[3]
datino = geolocator.geocode('Mokapu, United States')
datino.point.longitude
cities[3528]
cwd = os.getcwd()