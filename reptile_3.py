import io
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt  # for 畫圖用
import random

def crawl_price(stock_id):
    now = int(datetime.datetime.now().timestamp())+86400
    url = "https://query1.finance.yahoo.com/v7/finance/download/" + stock_id + "?period1=0&period2=" + str(now) + "&interval=1d&events=history&crumb=hP2rOschxO0"

    response = requests.post(url)
    #將資料存檔
    with open(str(stock_id)+'.csv', 'w') as f:
        f.writelines(response.text)
    print(response.text)
    f = io.StringIO(response.text)
    df = pd.read_csv(f, index_col='Date', parse_dates=['Date'] )
    return df

#爬蟲 歷史股價
#2480 連宇
#2330 台積電
#2354 鴻海
STOCK_ID = "2354.TW"
df = crawl_price(STOCK_ID)






import pandas as pd
# brfore:
# df = pd.read_csv('連宇歷史股價.csv')
# after:
df = pd.read_csv(str(STOCK_ID) + ".csv", index_col='Date', parse_dates=['Date'])

print(df.head())



# Visualising the results
plt.plot(df.Close, color = 'red', label = 'Real '+ str(STOCK_ID) + ' Price')  # 紅線表示真實股價
plt.title(str(STOCK_ID) + ' Price')
plt.xlabel('Date')
plt.ylabel(str(STOCK_ID) + ' Stock Price')
plt.legend()
plt.show()

