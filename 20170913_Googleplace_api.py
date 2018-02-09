
# 目前用的python套件：
# Github 頁面:

# https://github.com/slimkrazy/python-google-places

from googleplaces import GooglePlaces, types, lang
import pandas as pd

google_places = GooglePlaces(api_key)
# 輸入自己api_key

radar_result = (google_places.radar_search(language = 'zh-TW',
                                           lat_lng ={'lat':25.0513848,
                                                    'lng':121.5475527},
# 這邊是小巨蛋gps點                                 
                                           keyword = '室內設計',
                                           radius = 3000,
                                           location = '松山,台北'
# 設定範圍 單位公尺
                                          ))

for p in radar_result.places:
    p.get_details(language='zh-TW')
# 得到place的詳細資料
    
for i in range(0, len(radar_result.places)):
    print(radar_result.places[i])
# 印出來看看 
    
results = radar_result.places

result_list = []

for result in results:
    n_lat = float(result.geo_location['lat'])
    n_lng = float(result.geo_location['lng'])      
    n_name = result.name
    n_list = [n_name, n_lat, n_lng]
    result_list.append(n_list)
# Data clearning...
    
df_place = pd.DataFrame(result_list,columns=['name','lat','lng'])
# 利用pandas dataframe 將資料合併

