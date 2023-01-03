from binance import Client
import pandas as pd
import configparser
import os
from datetime import datetime
import dateutil.relativedelta

os.chdir(os.path.join(os.getcwd(),"Socket"))

config = configparser.ConfigParser()
config.read_file(open('config.cfg'))
PUBLIC_KEY = config.get('BINANCE', 'PUBLIC_KEY')
PRIVATE_KEY = config.get('BINANCE', 'PRIVATE_KEY')

if not os.path.exists('Last_Updated_Socket.txt'):
    last_updated_time = str(
        datetime.now() + dateutil.relativedelta.relativedelta(months=-1))
else:
    with open('Last_Updated_Socket.txt', 'r') as f:
        last_updated_time = f.read()

client = Client(PUBLIC_KEY, PRIVATE_KEY)
df = pd.DataFrame()

for coins in client.get_all_tickers():
    if((coins["symbol"][-4:] == "BUSD")):
        historical_data = client.get_historical_klines(
            symbol=coins["symbol"], interval=Client.KLINE_INTERVAL_4HOUR, start_str=last_updated_time)
        coin_df = pd.DataFrame(historical_data, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume',
                               'Close Time', 'Quote Asset Volume', 'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore'])
        coin_df["COIN"] = coins["symbol"][:-4]
        if not (coin_df.empty):
            coin_df["Values"] = coin_df[["COIN", "High", "Low"]].apply(lambda x: "-".join(x), axis=1)
            df = pd.concat([df, coin_df[["Open Time", "Values"]]], axis=0)
        df['Open Time'] = df['Open Time'].apply(lambda x: int(x)/1000)
        df['Open Time'] = pd.to_datetime(df['Open Time'], unit='s')

df.to_csv("../shared/Socket.csv", columns=["Open Time", "Values"], index=False)
with open('Last_Updated_Socket.txt', 'w') as f:
        f.write(last_updated_time)