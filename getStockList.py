import requests
import json
import pandas as pd

url = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
fileName = f"D:\\tmp\stock\\0_total.txt"
#關鍵字查詢
keyWord = ""

result = requests.get(url)
result.encoding ="utf-8"
statusCode = result.status_code

jsonObj = json.loads(result.text)

#json object to dataframe
df = pd.json_normalize(jsonObj)
df = df[["公司簡稱","公司代號"]]
if keyWord != "" : df = df[df['公司簡稱'].str.contains(keyWord)]

listName = df["公司簡稱"].tolist()
listCode = df["公司代號"].tolist()
listTotal = []
for idx,name in enumerate(listName):
    listTotal.append(f"{listCode[idx]}:{name}")

result = "".join( x + "\n" for x in listTotal)

#寫入檔案
f = open(fileName,'w', encoding='UTF-8')
f.write(result)
f.close()
