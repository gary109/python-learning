import requests
from io import StringIO
import pandas as pd
import numpy as np

datestr = '20180131'

# 下載股價
r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')

# 整理資料，變成表格
df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                     for i in r.text.split('\n') 
                                     if len(i.split('",')) == 17 and i[0] != '='])), header=0)

                              

cond1 = df[pd.to_numeric(df['本益比'], errors='coerce') < 15] 
cond1.to_csv('TW_Stock_Result.csv')
print(cond1)

 