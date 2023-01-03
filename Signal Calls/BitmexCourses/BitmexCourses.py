import pandas as pd
import re

colnames=['Name','Date','Time', 'Text','Cleaned_text'] 
exchanges = ['BINANCE', 'BYBIT', 'FTX', 'HUOBI', 'KUCOIN', 'POLONIEX','KRAKEN']
df = pd.read_csv('./1_BitmexCourses.csv',names = colnames,header=None)


exchanges = 'Binance|kucoin|bitbuy'
conversion = 'usdt|usd|btc|eth'
exchangeregex = '|'.join(exchanges)
target = ('|').join(['1','2','3'])
def extractor(i):
  text = re.sub('[\',\[\]]', '', i)
  coin_name,conversion_name,call_exchange,call_type,call_duration,leverage,Targets,stop_loss= ["None"]*8
  if(re.search('stop\s*loss',text,re.IGNORECASE) and re.search('target|targets',text,re.IGNORECASE)):    

    coin_name=re.findall('(\w+)(?:usdt|usd|btc|eth)',text,re.IGNORECASE)

    conversion_name = re.findall('\w+({})'.format(conversion),str(text),re.IGNORECASE)

    call_exchange = re.findall('Binance|kucoin|bitbuy'.format(exchanges),text,re.IGNORECASE)

    call_type = re.findall('sell|buy',text,re.IGNORECASE)

    """duration not used """
    call_duration = re.findall('long|short',text,re.IGNORECASE)

    """some targets are not extracted although format is same """
    Targets = re.findall("Target[s]*[ ]*(.*?)[a-zA-Z]",text,re.IGNORECASE)
    t = re.sub(' ','',Targets[0])
    Targets = t.split('-')


    leverage = re.findall('[ ]*[-]*[ ]*(\d+)x',text,re.IGNORECASE)

    """ stop loss not used that much"""
    stop_loss = re.findall('stop\s*loss\s*-*\s*(\d.\d*)',text,re.IGNORECASE)

    
  return [coin_name,conversion_name,call_exchange,call_type,call_duration,leverage,Targets,stop_loss]
  
df["Call"] = df['Cleaned_text'].apply(extractor)

def func(x):
    for i in range(len(x)):
        if (len(x[i])==1):
            x[i]=x[i][0]
        elif not (x[i]):
            x[i]="None"
    return x
df["Call"] = df["Call"].apply(func)


df = df.drop(columns=["Text"])
pd.to_pickle(df,"2_BitmexCourses.pkl")