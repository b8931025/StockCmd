import requests
from datetime import datetime
from bs4 import BeautifulSoup

#time
now = datetime.now() # current date and time
today = now.strftime("%Y") + now.strftime("%m") + now.strftime("%d") + now.strftime("%H") + now.strftime("%M") + now.strftime("%S")
#個股代號
stockId = 2603 
#檔案路徑
fileName = f"D:\\tmp\stock\\{stockId}-{today}-info.txt"
#log路徑
logName = f"D:\\tmp\stock\\log.txt"
#https://tw.stock.yahoo.com/quote/2317.TW
url = f"https://tw.stock.yahoo.com/quote/{stockId}.TW"
result = requests.get(url)
soup  = BeautifulSoup(result.text, 'html.parser')
#終端機輸出
showConsole = True  

#取得title
title = soup.find_all("h2",class_="Fz(20px)--mobile Fw(b) Fz(14px)")[0].text 
title += f"({stockId})"
#取得行情
infoArea = soup.find_all("ul",class_="D(f) Fld(c) Flw(w) H(192px) Mx(-16px)")
soup  = BeautifulSoup(str(infoArea), 'html.parser') #將soup範圍縮小

infoHtml = soup.select("li > span")
infoTexts = soup.select("li > span.C\(\#232a31\)")
infoValues = soup.select("li > span.Fw\(600\)")

fileContent = [title]
for idx, column in enumerate(infoTexts):
    fileContent.append(column.text + ":" + infoValues[idx].text)

#寫入檔案
result = ''.join(x + '\n' for x in fileContent)
if showConsole: print(result)
f = open(fileName,'w', encoding='UTF-8')
f.write(result)
f.close()

#log html
result = str(infoHtml).replace(", <li","\n, <li").replace(", <s",",\n <s") + "\n" + fileName + "\n"
f = open(logName,'a', encoding='UTF-8')
f.write(result)
f.close()
