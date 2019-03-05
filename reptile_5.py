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
    #with open(str(stock_id)+'.csv', 'w') as f:
    #    f.writelines(response.text)
    #print(response.text)
    f = io.StringIO(response.text)
    df = pd.read_csv(f, index_col='Date', parse_dates=['Date'] )
    return df

url = "https://finance.yahoo.com/world-indices/"
response = requests.get(url)

import io
f = io.StringIO(response.text)
dfs = pd.read_html(f)
world_index = dfs[0]


#print (dfs[0])

import time
world_index_history = {}
for symbol, name in zip(world_index['Symbol'], world_index['Name']):
    print(name)
    world_index_history[name] = crawl_price(symbol)
    time.sleep(5)

for name, history in world_index_history.items():   
    plt.plot(history.Close, color = (random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)), label = 'Real '+ str(name) + ' Price')  
plt.title('World Stock Price')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()