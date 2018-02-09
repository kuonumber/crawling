
# coding: utf-8

import pandas as pd
import requests
from bs4 import BeautifulSoup
import googlemaps
from datetime import datetime
from tqdm import tqdm_notebook
import json
from selenium import webdriver
driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs')

gmaps = googlemaps.Client(key='API_KEY')

yourator_api_url = 'https://www.yourator.co/api/v2/companies?area[]=1'

yourator_taipei_companies = []
for area_code in range(1,2):
    for page in range(1,13):
        res = requests.get('https://www.yourator.co/api/v2/companies?area[]={}&page={}'.format(area_code,page))
        df_taipei_com = pd.DataFrame(res.json()['companies'])
        yourator_taipei_companies.append(df_taipei_com)


df_taipei_companies = pd.concat(yourator_taipei_companies)

df_yourator_taipei_companies = df_taipei_companies.reset_index(drop=True)


def take_tags(tags):
    tag_ = [tag['name']for tag in tags]
    return tag_
def take_cat(cats):
    cats_ = cats['name'].split('/')
    return cats_

df_yourator_taipei_companies['tags_'] = df_yourator_taipei_companies.tags.apply(take_tags)

df_yourator_taipei_companies['category_'] = df_yourator_taipei_companies.category.apply(take_cat)

yourator_url  = 'https://www.yourator.co/'

df_yourator_taipei_companies['path_'] = yourator_url + df_yourator_taipei_companies['path']


def get_basic_info(web_path):
    res = requests.get(web_path)
    soup = BeautifulSoup(res.text,'lxml')
    soup_ = soup.select('.basic-info')
    company_basic_info = [basic_info.text for basic_info in soup_]
    return company_basic_info

df_yourator_taipei_companies['basic_info'] = df_yourator_taipei_companies.path_.apply(get_basic_info)

def get_address(info):
    address = info[1].split('：')[1].strip()
    return address

df_yourator_taipei_companies['address'] = df_yourator_taipei_companies.basic_info.apply(get_address)

list_geocode = ([gmaps.geocode(loc,language='zh-TW') 
                for loc in tqdm_notebook(df_yourator_taipei_companies.address)])

lat_lng = []
for place in list_geocode:
    try:
        lat_lng.append(place[0]['geometry']['location'])
    except:
        lat_lng.append(None)
        pass

lat_lng_ = []
for v in lat_lng:
    try:
        lat_lng_.append(tuple(v.values())) 
    except:
        lat_lng_.append('None')
        pass

df_yourator_taipei_companies['lng_lat'] = pd.Series(lat_lng_)


# (df_yourator_taipei_companies[['brand','description','tags_',
                              # 'path_','category_', 'basic_info',
                              # 'address','lng_lat']])


df_yourator_taipei_companies.to_csv('./inVisibleCity/df_yourator_taipei_companies_20180206.csv')

