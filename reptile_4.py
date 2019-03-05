import io
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt  # for 畫圖用

url = "https://finance.yahoo.com/world-indices/"
response = requests.get(url)

import io
f = io.StringIO(response.text)
dfs = pd.read_html(f)
world_index = dfs[0]


print (dfs[0])
