from types import NoneType
from matplotlib.pyplot import show
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import pandas as pd

#取得觀察個股清單
def getStockList():
    result = []
    #讀檔
    f = open("0_list.txt","r", encoding='UTF-8')
    for line in f.readlines():
        result.append(line.split(":")[0])
    f.close()
    return result

#取得個股即時資訊
def getStockInfo(stockId):
    url = f"https://tw.stock.yahoo.com/quote/{stockId}"
    result = requests.get(url)
    soup  = BeautifulSoup(result.text, 'html.parser')
    title = soup.title
    cssInfo = "D(f) Fld(c) Flw(w) H(192px) Mx(-16px)"

    if type(title) is NoneType:
        return f"查無該股({stockId})資訊"

    #取得title
    infos = [title.getText().split(" 走勢")[0]]
    #取得行情
    infoArea = soup.find_all("ul",class_=cssInfo)
    soup  = BeautifulSoup(str(infoArea), 'html.parser') #將soup範圍縮小
    infoTexts = soup.select("li > span.C\(\#232a31\)")
    infoValues = soup.select("li > span.Fw\(600\)")

    columns = []
    for idx, column in enumerate(infoTexts):
        if (column.text == "成交" or 
            column.text == "漲跌幅" or 
            column.text == "漲跌" or 
            column.text == "昨收" ):
            columns.append(column.text + ":" + infoValues[idx].text)

    #sort
    infos.append(columns[0]) #成交
    infos.append(columns[3]) #漲跌
    infos.append(columns[2]) #漲跌幅
    infos.append(columns[1]) #昨收

    #輸出結果
    return '\t'.join(x for x in infos)

#取得大盤資訊
def getTWII():
    url = "https://tw.stock.yahoo.com/quote/^TWII"
    req = requests.get(url)
    req.encoding = 'utf-8'
    output = ["加權指數"]

    #get json data
    jsonObj = ""
    jsonTxt = ""
    for x in req.text.split("\n"):
        if "root.App.main" in x : 
            #去掉前面
            x = x.replace("root.App.main = ","")
            #去掉最後的;號
            x = x[0:len(x)-1] 
            #undefined 改成字串
            jsonTxt = x.replace("undefined",'""')
    jsonObj = json.loads(jsonTxt)
    jsonObj = jsonObj["context"]["dispatcher"]["stores"]["QuoteFundamental"]["quote"]["data"]

    output.append(f"漲跌:{jsonObj['change']}")
    output.append(f"漲跌幅:{jsonObj['changePercent']}")
    output.append(f"成交價:{jsonObj['price']}")
    output.append(f"前日收盤價:{jsonObj['regularMarketPreviousClose']}")
    output.append(f"開盤價:{jsonObj['regularMarketOpen']}")

    return '\t'.join(output)

#取得公司名稱與股票代號清單
def getCompanyList(keyWord = ""):
    url1 = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
    url2 = "https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes"
    listTotal = []
    
    #上市資料
    result = requests.get(url1)
    result.encoding ="utf-8"
    jsonObj1 = json.loads(result.text)

    #json object to dataframe
    df = pd.json_normalize(jsonObj1)
    df = df[["公司簡稱","公司代號"]]
    if keyWord != "" : df = df[df['公司簡稱'].str.contains(keyWord)]

    listName = df["公司簡稱"].tolist()
    listCode = df["公司代號"].tolist()
    for idx,name in enumerate(listName):
        listTotal.append(f"{listCode[idx]}:{name}")

    #上櫃資料
    result = requests.get(url2)
    result.encoding ="utf-8"
    jsonObj2 = json.loads(result.text)

    #json object to dataframe
    df = pd.json_normalize(jsonObj2)
    df.rename(columns = {'SecuritiesCompanyCode':'公司代號', 'CompanyName':'公司簡稱'}, inplace = True)
    df = df[["公司簡稱","公司代號"]]
    if keyWord != "" : df = df[df['公司簡稱'].str.contains(keyWord)]

    listName = df["公司簡稱"].tolist()
    listCode = df["公司代號"].tolist()
    for idx,name in enumerate(listName):
        listTotal.append(f"{listCode[idx]}:{name}")

    return "\n".join(listTotal)    