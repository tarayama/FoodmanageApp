import geocoder
from geopy.distance import distance
import pandas as pd
import numpy as np
import re
import json

#フードバンクのデータ
df = pd.read_csv('foodmanager/data/FoodBankListo.csv') #djangoはmanage.pyが実行しているのでそこから起点で考える

#郵便データ
postal_df = pd.read_csv('foodmanager/data/KEN_ALL.CSV', encoding="shift-jis")

#大まかな住所から緯度経度を返す
def get_lat_lon_from_address(address):
    ret = geocoder.osm(address)
    return ret.latlng


#2点の緯度経度情報から距離を返す(km)
def get_distance_from_lat_lon(loc1, loc2):
    dist = distance(loc1,loc2).km
    return dist


#郵便番号(文字列型)から大まかな住所を返す
#ハイフンありでも可
#伊達市,府中市は都道府県名を含んで返す
def get_address(str_userpcode):
    int_userpcode = int(re.sub('[^0-9]','', str_userpcode))
    add = postal_df[postal_df["PostalCode"]==int_userpcode]["Address"].item()
    if add == "伊達市":
        add = postal_df[postal_df["PostalCode"]==int_userpcode]["Prefectures"].item() + add
    elif add == "府中市":
        add = postal_df[postal_df["PostalCode"]==int_userpcode]["Prefectures"].item() + add
    return add


#郵便番号から近くのフードバンク情報を5件を返す
def get_near_foodbanks(user_pcode):    
    df_lat_lon = df["NorthLa-EastLon"]
    useradd = get_address(user_pcode)
    userlatlon = get_lat_lon_from_address(useradd)
    latlons = []
    for a in df_lat_lon:
        latlons.append(get_distance_from_lat_lon(a.replace('[', '').replace(']', '').split(','), userlatlon))
    df["distance_from_user"]=latlons
    return df.sort_values(by='distance_from_user').head().to_json(orient='records')
    #return行の末尾に".to_json(force_ascii=False)"を追加すればjson型で返す

def Dataframetodict(dataframe):
    result = []
    for i in range(5):
        
        result.append(dict(dataframe.iloc[i]))
    return result

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(JsonEncoder, self).default(obj)
    
def main():
    postal_code = "176-0013"
    df = get_near_foodbanks(postal_code)
    display(df)
    dict = Dataframetodict(df)
    print(dict)
    
if __name__ == "__main__":
    main()
