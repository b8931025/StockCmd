from sre_constants import JUMP
from stock import *
import sys

'''
#問題
價跌時沒有負號


'''

#所有各股
fileNameAllCompany = ".\\0_total.txt"
#即時資訊
fileNameDailyStockInfo = ".\\0_dailyStockInfo.txt"
#是否顯示在終端機
showConsole = True

#功能說明 
msgHelp = '''
功能參數
-m         :  取得即時股市資訊-觀察清單
-i  stockId:  取得即時個股報價
-q  keyWord:  查詢公司名稱與股票代號
-list      :  列出上市櫃所有各股
'''

def show(txt):
    if showConsole : print(txt)

def main():
    #大盤
    twMarket = getTWII()
    show(twMarket)
    fileData = [twMarket]

    #觀查個股
    list = getStockList()
    for stockId in list:
        _stock = getStockInfo(stockId)
        show(_stock)
        fileData.append(_stock)

    #寫入檔案
    openTextMode = "w" # w:write a:append r:read
    f = open(fileNameDailyStockInfo,openTextMode, encoding='UTF-8')

    #append模式就換行
    if (openTextMode == "a"): f.write("\n")
    f.write("\n".join(fileData))
    f.close()

if __name__ == '__main__':
    args = sys.argv
    argsLen = len(args)
    arg1 = ""
    arg2 = ""
    if argsLen > 1 : arg1 = args[1]
    if argsLen > 2 : arg2 = args[2]

    if arg1 == "-m" :
        #取得即時股市資訊-觀察清單
        main()
    elif arg1 == "-q" :
        #查詢公司名稱與股票代號
        if arg2 == "" :
            print("請輸入查詢關鍵字")
        else:
            list = getCompanyList(arg2)
            print(list)
    elif arg1 == "-list" :
        #列出上市櫃所有各股
        list = getCompanyList("")
        print(list)
        #寫入檔案
        f = open(fileNameAllCompany,"w", encoding='UTF-8')
        f.write(list)
        f.close()
    elif arg1 == "-i":
        #取得即時個股報價
        if arg2 == "" :
            print("請輸入個股代號")
        else:    
            print(getStockInfo(arg2))
    else:
        print(msgHelp)
