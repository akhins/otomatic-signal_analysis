import requests
import json
import time

url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'

response = requests.get(url)
data = json.loads(response.text)

symbols = set([d['symbol'] for d in data['symbols']])
symbols_found = set()


url = 'https://fapi.binance.com/fapi/v1/klines?interval=4h&symbol={}'

while True:
    for symbol in symbols:
   
        response = requests.get(url.format(symbol))
        data = json.loads(response.text)

        
        for i in range(len(data)-1):
            current_close = float(data[i][4])
            current_high = float(data[i][2])
            current_low = float(data[i][3])
            next_close = float(data[i+1][4])
            next_high = float(data[i+1][2])
            next_low = float(data[i+1][3])
            if current_close > current_high and next_close < next_low:
                if symbol not in symbols_found:
                    symbols_found.add(symbol)
                    print(symbol + ": 🔥Pozitif Uyumsuzluk Tespit Edildi🔥")
            elif current_close < current_low and next_close > next_high:
                if symbol not in symbols_found:
                    symbols_found.add(symbol)
                    print(symbol + ": 🔥Negatif Uyumsuzluk Tespit Edildi🔥")
        time.sleep(3600)
