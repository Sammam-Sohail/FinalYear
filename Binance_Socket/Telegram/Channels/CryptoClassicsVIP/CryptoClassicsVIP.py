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
        df = pd.read_csv('./1_CryptoClassicsVIP.csv',names = colnames,header=None)
        exchanges = 'Binance|kucoin|bitbuy'
        conversion = 'usdt|usd|btc|eth'
        exchangeregex = '|'.join(exchanges)
        target = ('|').join(['1','2','3'])
        def extractor(text):
          Targets = None
          if(re.search('\w+({})'.format(conversion),text,re.IGNORECASE) and re.search('target',text,re.IGNORECASE)):    
            Name=re.findall('(\w+)(?:usdt|usd|btc|eth)',text,re.IGNORECASE)[0].upper()
            Conversion = getFirst(re.findall('\w+({})'.format(conversion),str(text),re.IGNORECASE)).upper()
            Exchange = getFirst(re.findall('\w+({})'.format(exchanges),text,re.IGNORECASE))
            Type = getFirst(re.findall('sell|buy',text,re.IGNORECASE))
            Duration = getFirst(re.findall('long|short',text,re.IGNORECASE)).upper()
            Entry = getFirst([float(x) for tup in re.findall(r"(?<=Entry zone )(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(?=Amount)", text)for x in tup])
            Leverage = getFirst(re.findall('[ ]*[-]*[ ]*(\d+)x',text,re.IGNORECASE))
            Targets= getFirst([float(x) for tup in re.findall(r'target\s*[0-9]\s*(\d+(?:\.\d+)?)\s*[0-9]\s*(\d+(?:\.\d+)?)\s*[0-9]\s*(\d+(?:\.\d+)?)',text,re.IGNORECASE)for x in tup])
            Stoploss = getFirst([float(i) for i in re.findall('stop\s*(\d+(?:\.\d+)?)',text,re.IGNORECASE)])
            return {
                "Status":"A",
                "Coin": Name,
                "Conversion": Conversion,
                "Exchange": Exchange,
                "Type": Type,
                "Duration": Duration,
                "Entry":Entry,
                "Targets": Targets,
                "Stoploss": Stoploss,
                "Leverage": Leverage,
                "CompletedOn":"",
                }

        df['Call']= df['Cleaned_text'].apply(extractor)
          
        df = df.drop(columns=["Text"])
        
        if not os.path.exists(f"{Root_PATH}/shared/Calls/{folder_name}"):
          os.mkdir(f"{Root_PATH}/shared/Calls/{folder_name}")

        pd.to_pickle(df,f"{Root_PATH}/shared/Calls/{folder_name}/2_{folder_name}.pkl")
        print("CryptoClassicsVIP Scraped")