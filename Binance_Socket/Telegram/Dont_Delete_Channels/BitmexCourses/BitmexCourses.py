import pandas as pd
import re
import os
from csv import writer

Root_PATH = os.getcwd()
for Folder_Name in os.listdir(os.path.join(os.getcwd(),"Telegram","Channels")):
    if (str(os.path.basename(__file__)).split(".")[0] == Folder_Name):
        os.chdir(os.path.join(os.getcwd(),"Telegram","Channels",Folder_Name))
        folder_name = os.path.basename(os.getcwd())
        colnames=['Name','Date','Time', 'Text','Cleaned_text'] 
        exchanges = ['BINANCE', 'BYBIT', 'FTX', 'HUOBI', 'KUCOIN', 'POLONIEX','KRAKEN']
        df = pd.read_csv('./1_BitmexCourses.csv',names = colnames,header=None)
        exchanges = 'Binance|kucoin|bitbuy'
        conversion = 'usdt|usd|btc|eth'
        exchangeregex = '|'.join(exchanges)
        target = ('|').join(['1','2','3'])
        def extractor(i):
          text = re.sub('[\',\[\]]', '', i)

          if(re.search('stop\s*loss',text,re.IGNORECASE) and re.search('target|targets',text,re.IGNORECASE)):    
            coin_name=re.findall('(\w+)(?:usdt|usd|btc|eth)',text,re.IGNORECASE)
            conversion_name = re.findall('\w+({})'.format(conversion),str(text),re.IGNORECASE)
            call_exchange = re.findall('Binance|kucoin|bitbuy'.format(exchanges),text,re.IGNORECASE)
            call_type = re.findall('sell|buy',text,re.IGNORECASE)
            call_duration = re.findall('long|short',text,re.IGNORECASE)
            targets_regex = re.compile(r'Targets\s+([\d.-]+)\s*-\s*([\d.-]+)\s*-\s*([\d.-]+)\s*-\s*([\d.-]+)')
            matches = targets_regex.search(text)
            if matches:
                Targets = [match.strip() for match in matches.groups()]
            leverage = re.findall('[ ]*[-]*[ ]*(\d+)x',text,re.IGNORECASE)
            stop_loss = re.findall('stop\s*loss\s*-*\s*(\d.\d*)',text,re.IGNORECASE)

            with open('C:\\Users\\Mohib\\Desktop\\Testing Channels\\Channels\\BitmexCourses\\3_BitmexCourses.csv', 'a',newline='') as f_object:
              writer_object = writer(f_object)
              ls = [coin_name,conversion_name,leverage,call_exchange,call_type,call_duration,Targets,stop_loss]
              writer_object.writerow(ls)
              f_object.close()

          return i
  
        df['Cleaned_text'].apply(extractor)
          
        df["Call"] = df['Cleaned_text'].apply(extractor)

        df = df.drop(columns=["Text"])
        
        if not os.path.exists(f"{Root_PATH}\\shared\\Calls\\{folder_name}"):
          os.mkdir(f"{Root_PATH}\\shared\\Calls\\{folder_name}")

        pd.to_pickle(df,f"{Root_PATH}\\shared\\Calls\\{folder_name}\\2_{folder_name}.pkl")
        print("BitmexCourses Scraped")