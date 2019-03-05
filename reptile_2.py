import requests
import matplotlib.pyplot as plt  # for 畫圖用
import random
import numpy as np

#爬蟲 連宇歷史股價

res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")

#2480 連宇
#2330 台積電
site = "https://query1.finance.yahoo.com/v7/finance/download/2480.TW?period1=0&period2=1549258857&interval=1d&events=history&crumb=hP2rOschxO0"
response = requests.post(site)

print(response.text)

#將資料存檔
with open('2480.TW.csv', 'w') as f:
    f.writelines(response.text)

import pandas as pd
# brfore:
# df = pd.read_csv('連宇歷史股價.csv')
# after:
df = pd.read_csv('2480.TW.csv', index_col='Date', parse_dates=['Date'])

print(df.head())



# Visualising the results
plt.plot(df.Close, color = (random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)), label = 'Real Uniform Stock Price') 
plt.title('Uniform Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Uniform Stock Price')
plt.legend()
plt.show()

