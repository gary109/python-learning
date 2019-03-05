# Step 1: 資料前處理
# Import the libraries
import numpy as np
import matplotlib.pyplot as plt  # for 畫圖用
import pandas as pd

# Import the training set
dataset_train = pd.read_csv("uniform_stock_train.csv")  # 讀取訓練集
training_set = dataset_train.iloc[:, 1:2].values  # 取「Open」欄位值
print (training_set)

# Feature Scaling
from sklearn.preprocessing import MinMaxScaler

sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

X_train = []   #預測點的前 60 天的資料
y_train = []   #預測點
for i in range(60, 4262):  # 4262 是訓練集總數
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)  # 轉成numpy array的格式，以利輸入 RNN

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))


#Step 2: 搭建一個 LSTM 魔法陣
# Import the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.models import load_model
import os


# load model
# Initialising the RNN
regressor = Sequential()

# 要檢查的檔案路徑
filename = "uniform_stock_model.h5"
print('load model ...')
# 檢查檔案是否存在
if os.path.isfile(filename):
  regressor = load_model('uniform_stock_model.h5')
else:
    print('build model ...')
    # Adding the first LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
    regressor.add(Dropout(0.2))

    # Adding a second LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units = 50, return_sequences = True))
    regressor.add(Dropout(0.2))

    # Adding a third LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units = 50, return_sequences = True))
    regressor.add(Dropout(0.2))

    # Adding a fourth LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units = 50))
    regressor.add(Dropout(0.2))

    # Adding the output layer
    regressor.add(Dense(units = 1))

    # Compiling
    regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')
    
    # 進行訓練
    print('train model ...')
    regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)

    # save
    print('test before save: ', regressor.predict(X_test[0:2]))
    regressor.save('uniform_stock_model.h5')   # HDF5 file, you have to pip3 install h5py if don't have it


#Step 3: 進行預測
dataset_test = pd.read_csv('uniform_stock_test.csv')
real_stock_price = dataset_test.iloc[:, 1:2].values

dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs) # Feature Scaling

X_test = []
for i in range(60, 80):  # timesteps一樣60； 80 = 先前的60天資料+2018年的20天資料
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))  # Reshape 成 3-dimension


#進行預測
print('predict model ...')
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)  # to get the original scale

# Visualising the results
plt.plot(real_stock_price, color = 'red', label = 'Real Uniform Stock Price')  # 紅線表示真實股價
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted Uniform Stock Price')  # 藍線表示預測股價
plt.title('Uniform Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Uniform Stock Price')
plt.legend()
plt.show()

del regressor  # deletes the existing model