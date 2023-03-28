import pandas as pd
import re
import os
Root_PATH = os.getcwd()
for Folder_Name in os.listdir(os.path.join(os.getcwd(),"Telegram","Channels")):
    if (str(os.path.basename(__file__)).split(".")[0] == Folder_Name):
        os.chdir(os.path.join(os.getcwd(),"Telegram","Channels",Folder_Name))

        folder_name = os.path.basename(os.getcwd())

        colnames=['Name','Date','Time', 'Text','Cleaned_text'] 
        exchanges = ['BINANCE', 'BYBIT', 'FTX', 'HUOBI', 'KUCOIN', 'POLONIEX','KRAKEN']
        df = pd.read_csv('./1_binancefuturesignal.csv',names = colnames,header=None)
        print(df['Cleaned_text'][0])
        print(df['Text'][0])
        df.head()

        exchanges = 'Binance|kucoin|bitbuy'
        conversion = 'usdt|usd|btc|eth'
        exchangeregex = '|'.join(exchanges)
        target = ('|').join(['1','2','3'])
        # coins=''
        def extractor(i):
          text = re.sub('[\',\[\]]', '', i)
          coin_name,conversion_name,call_exchange,call_type,call_duration,leverage,targets,stop_loss= ["None"]*8
          if(re.search('free signal|entry point',text,re.IGNORECASE) and re.search('target|targets',text,re.IGNORECASE)):    

            coin_name=re.findall('(\w+){}'.format(conversion),text,re.IGNORECASE)
            
            conversion_name = re.findall('\w+({})'.format(conversion),str(text),re.IGNORECASE)
            
            """exchange not used"""
            call_exchange = re.findall('\w+({})'.format(exchanges),text,re.IGNORECASE)
            
            call_type = re.findall('sell|buy',text,re.IGNORECASE)

            range =  re.findall(r'around\s+(\d+(?:\.\d+)?\s*-\s*\d+(?:\.\d+)?)',text,re.IGNORECASE)
            """duration not used that much"""
            call_duration = re.findall('long|short',text,re.IGNORECASE)
            """current not given, between is given"""
            # current_value=re.findall('')

            # leverage = re.findall('leverage\s*-*\s*(\d.*x)',text,re.IGNORECASE)
            leverage = re.findall('[ ]*[-]*[ ]*(\d+)x',text,re.IGNORECASE)
            # if (leverage): leverage = str(leverage[0]).split()

            """some targets are not extracted although format is same """
            targets=re.findall(r'Targets\s+(\d+(?:\.\d+)?(?:\s*-\s*\d+(?:\.\d+)?)+)',text,re.IGNORECASE)
            if targets:
              targets = [t.strip() for t in targets[0].split('-')]
            
            """ stop loss not used that much"""
            stop_loss = re.findall('stop\s*loss\s*-*\s*(\d.\d*)',text,re.IGNORECASE)

            
          return (coin_name,conversion_name,call_exchange,call_type,call_duration,leverage,targets,stop_loss)
        
        df["Call"] = df['Cleaned_text'].apply(extractor)

        df1 = df.copy()
        df1 = df1.drop(columns=["Text","Cleaned_text"])

        if not os.path.exists(f"{Root_PATH}\\shared\\Calls\\{folder_name}"):
          os.mkdir(f"{Root_PATH}\\shared\\Calls\\{folder_name}")

        pd.to_pickle(df,f"{Root_PATH}\\shared\\Calls\\{folder_name}\\2_{folder_name}.pkl")


