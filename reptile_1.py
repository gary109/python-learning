#如何獲得上市上櫃股票清單

import requests

res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")


#將網頁轉成 DataFrame
import pandas as pd

df = pd.read_html(res.text)[0]

# 整理資料 1 整理column名稱
# 設定column名稱
df.columns = df.iloc[0]
# 刪除第一行
df = df.iloc[1:]

# 整理資料 2 刪除冗餘行列
# 先移除row，再移除column，超過三個NaN則移除
df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)

# 設定index
df = df.set_index('有價證券代號及名稱')

print(df)