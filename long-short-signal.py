import requests
import json
import talib
import numpy as np
import time 

url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
symbols = requests.get(url).json()['symbols']

symbols = [symbol for symbol in symbols if symbol['symbol'] != 'BUSD']

while True:

    for symbol in symbols:
        symbol = symbol['symbol']
        url = f"https://fapi.binance.com/fapi/v1/klines?interval=4h&symbol={symbol}"
        data = requests.get(url).json()
        if not data:
            continue
        open_prices = np.array([float(d[1]) for d in data])
        high_prices = np.array([float(d[2]) for d in data])
        low_prices = np.array([float(d[3]) for d in data])
        close_prices = np.array([float(d[4]) for d in data])
        rsi = talib.RSI(close_prices, timeperiod=14)
        momentum = talib.MOM(close_prices, timeperiod=10)
    
        fastk, fastd = talib.STOCHRSI(close_prices, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        stoch_rsi = fastd[-1]                             
        
        if rsi[-1] >= 70 and stoch_rsi >= 80 and momentum[-1] > 0:
            print(symbol+": 👽Short👽 ")
        elif rsi[-1] <= 30 and stoch_rsi <=20 and momentum[-1] < 0:
            print(symbol+": 🔥Long🔥")
            print("-"*30)

    time.sleep(3600)
    print("-"*30)
