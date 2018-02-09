# coding: utf-8
# # Accupass


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tqdm import tqdm_notebook
import requests
import json
import csv
import datetime
import time


before = datetime.datetime.now()

活動已經結束網址 = 'https://old.accupass.com/search/r/1/0/5/0/4/{}/00010101/99991231?q=%E5%89%B5%E6%84%8F'

driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs')

for page in tqdm_notebook(range(0,3804)):
#    total 3804 pages 
    print(page)
    活動已經結束網址分頁 = 活動已經結束網址.format(page)
    driver.get(活動已經結束網址分頁)
    time.sleep(np.random.randint(1,4))
    pageSource = driver.page_source
#print(pageSource)
    soup = BeautifulSoup(pageSource, "lxml")

    for item_no in range(0,len(soup.select('.apcss-activity-card.ng-isolate-scope'))):
# event_number
        try:
            web_content = soup.select('.apcss-activity-card.ng-isolate-scope')[item_no]
            activity_event_number = web_content.select('.apcss-activity-card-body.ng-binding a')[0]['href'].split('/')[-1]
            page_likes = web_content.select('.apcss-activity-card-like.ng-binding')[0].text.split()[0]
            page_views = web_content.select('.apcss-activity-pageview.ng-binding')[0].text.split()[0]
            api_url = 'https://api.accupass.com/v3/events/{}'.format(activity_event_number) 
            res = requests.get(api_url)
    #       ----------------------------------------------------------
            res_json = res.json()
            title = res_json.get('title','')
            tags = [tag['name']  for tag in res_json.get('tags','')]
            cat = res_json.get('category','')['name'] 
            full_time = res_json['fullDateTimeStr']
            price = res_json['priceText']
            address = res_json['address']
            lng = res_json['location']['longitude']
            lat = res_json['location']['latitude']
            host = res_json['organizer']['title']
            des = [res_json.get('description','')]

    #       -------------------------------------------------------------
            intro = [activity_event_number,page_likes,page_views,
                     title,tags,cat,full_time,price,lng,lat,host,des]
    #         if activity_title==None:
    #             print(page)
    #         with open('./黑客松/已經結束活動.log','a',encoding='utf8') as l:
    #             l.writelines([str(page),activity_title])
            with open('./黑客松/accupass_all創意類活動_2018_02.csv','a',encoding='utf8') as f:
                w = csv.writer(f)
                w.writerow(intro)
        except:
            pass

after = datetime.datetime.now()
print ('總共花費時間：'+ str(after-before))
driver.close()




column = ['activity_event_number','page_likes','page_views',
    'title','tags','cat','full_time','price','lng','lat','host','des']


df_accupass_all創意類活動 = pd.read_csv('./黑客松/accupass_all創意類活動_2018_02.csv',names=column)


def time_transfer(full_time):

    if len(full_time)<=25:
#   單日
        start_date  = full_time.split()[0].split('(')[0]
        end_date = full_time.split()[0].split('(')[0]
        start_time = full_time.split()[1].split('~')[0]
        end_time = full_time.split()[1].split('~')[1]
#   跨日
    else:
        start_date = df.full_time[2].split()[0].split('(')[0]
        end_date = df.full_time[2].split()[3].split('(')[0]
        start_time =  df.full_time[2].split()[1]
        end_time = df.full_time[2].split()[-1]
    time_transfered = [start_date,end_date,start_time,end_time]
    return time_transfered





df_time_transfered =  pd.DataFrame([date_time for date_time in df.full_time.apply(time_transfer)],
            columns=['start_date','end_date','start_time','end_time'])

df_accuss_taipei = pd.concat([df_accupass_all創意類活動,df_time_transfered],axis=1)

df_accuss_taipei['is_holiday'] = df_accuss_taipei.full_time.str.contains('六|日')

df_accuss_taipei.to_csv('./inVisibleCity/20170207_accupass_Taipei_創意類別.csv')



