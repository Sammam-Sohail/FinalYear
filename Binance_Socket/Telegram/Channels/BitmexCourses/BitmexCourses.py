import pandas as pd
import re
import os

def getFirst(arr):
    if(len(arr) == 1):
        return arr[0]
    elif(len(arr)==0):
      return None
    else:
      return arr
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
        def extractor(text):
          Targets = None
          if(re.search('stop\s*loss',text,re.IGNORECASE) and re.search('target|targets',text,re.IGNORECASE)):    
            coin_name=getFirst(re.findall('(\w+)(?:usdt|usd|btc|eth)',text,re.IGNORECASE))
            conversion_name = getFirst(re.findall('\w+({})'.format(conversion),str(text),re.IGNORECASE))
            call_exchange = getFirst(re.findall('Binance|kucoin|bitbuy'.format(exchanges),text,re.IGNORECASE))
            call_type = getFirst(re.findall('sell|buy',text,re.IGNORECASE))
            call_duration = getFirst(re.findall('long|short',text,re.IGNORECASE))
            targets_regex = re.compile(r'Targets\s+([\d.-]+)\s*-\s*([\d.-]+)\s*-\s*([\d.-]+)\s*-\s*([\d.-]+)')
            matches = targets_regex.search(text)
            if matches:
                Targets = [float(match.strip()) for match in matches.groups()]
            leverage = getFirst([float(i) for i in re.findall('[ ]*[-]*[ ]*(\d+)x',text,re.IGNORECASE)])
            stop_loss = getFirst([float(i)for i in re.findall('stop\s*loss\s*-*\s*(\d.\d*)',text,re.IGNORECASE)])
          return {
              "Status":"A",
              "Coin": coin_name,
              "Conversion": conversion_name,
              "Exchange": call_exchange,
              "Type": call_type,
              "Duration": call_duration,
              "Targets": Targets,
              "Stoploss": stop_loss,
              "Leverage": leverage,
              "CompletedOn":"",
            }

        df['Call']= df['Cleaned_text'].apply(extractor)
          
        df = df.drop(columns=["Text"])
        
        if not os.path.exists(f"{Root_PATH}/shared/Calls/{folder_name}"):
          os.mkdir(f"{Root_PATH}/shared/Calls/{folder_name}")

        pd.to_pickle(df,f"{Root_PATH}/shared/Calls/{folder_name}/2_{folder_name}.pkl")
        print("Bitmex Scraped")