import json
import requests
import xml.etree.ElementTree as ET

yahoo_client_id = 'dj00aiZpPWFzd2tQN1NCUG1HbSZzPWNvbnN1bWVyc2VjcmV0Jng9ZWQ-' #yahoo! network service

class FoodName():
    def __init__(self, jancode):
        self.jancode = jancode
        self.name = ""
    
    #Yahooの商品検索APIで商品名を取得
    def setYahooProductName(self):
        baseurl = "http://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"
        params = {
            'appid' : yahoo_client_id,
            'jan_code' : self.jancode
        }
        response = requests.get(baseurl, params=params)
        values = json.loads(response.text)
        self.name = values.get("hits")[0].get("name")
    
    #Yahooの形態素解析APIを実行
    def setShorterFoodName(self):
        baseurl = "https://jlp.yahooapis.jp/KeyphraseService/V1/extract"
        params = {
            'appid' : yahoo_client_id,
            'sentence' : self.name
        }
        response = requests.get(baseurl, params=params)
        resxml = response.text
        root = ET.fromstring(resxml)
        #点数の良い上位二個をつなげて1文にする
        foodname = root[0][0].text + root[1][0].text
        foodname = ''.join(foodname.splitlines())
        self.name = foodname
    
    def setName(self, string):
        self.name = string
    
    def getName(self):
        return self.name
        
