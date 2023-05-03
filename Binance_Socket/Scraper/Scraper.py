import re
import string
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import os
import numpy as np
from datetime import datetime
import ast
import configparser
import snscrape.modules.telegram as telegram
import pandas as pd

if not os.path.exists('Last_Updated.txt'):
    prev_month = datetime.now().replace(month=datetime.now().month-1)
    if prev_month.month == 12:
        prev_month = prev_month.replace(year=prev_month.year-1)   
    extractiontimestamp = int(datetime.strptime(str(prev_month).split(".")[0], "%Y-%m-%d %H:%M:%S").timestamp())
else:
    with open('Last_Updated.txt', 'r') as f:
        last_updated_time = f.read()
        CurrentYear,CurrentMonth,CurrentDate = [int(i) for i in last_updated_time.split(" ")[0].split("-")]


config = configparser.ConfigParser()
config.read_file(open('config.cfg'))
binance_coins= ast.literal_eval(config.get('Telegram', 'Coins'))
groups = ast.literal_eval(config.get('Telegram', 'Groups'))




tweets_list = []
for i in groups:
    for x,tel in enumerate(telegram.TelegramChannelScraper(i).get_items()):
        telegramTimestamp = int(datetime.strptime(str(tel.date)[:-6], "%Y-%m-%d %H:%M:%S").timestamp())
        if extractiontimestamp > telegramTimestamp:
            break
        tweets_list.append([i,telegramTimestamp, tel.content])
    
    
tel_df = pd.DataFrame(tweets_list, columns=['Name','Timestamp','Text'])

def MoreCleaning(text):
    if(text!= None):
        str_en = text.encode("ascii", "replace").replace(b"?",b" ")
        str_de = str_en.decode()
        str_de = re.sub(' +', ' ', re.sub(r"([0-9]+(\.[0-9]+)?)",r" \1 ", str_de).strip())
        str_de = re.sub(r"\bStop\sLoss\b", "StopLoss", str_de,re.IGNORECASE)
        matches = re.findall(r"\btarget[s]?\b", str_de,re.IGNORECASE)
        if matches:
            return str_de
        else:
            return np.nan
tel_df["Text"] = tel_df["Text"].apply(MoreCleaning)

tel_df= tel_df.iloc[::-1]


stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
exclude.remove('.')
exclude.remove('-')
lemma = WordNetLemmatizer()
def text_cleaning(text):
    stop_free = ' '.join([word for word in str(text).split() if word not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = ' '.join([lemma.lemmatize(word) for word in punc_free.split()])
    return normalized

tel_df["Cleaned Text"]= tel_df["Text"].apply(text_cleaning)

os.chdir('C:\\Users\\Mohib\\Desktop\\Testing Channels')
if not os.path.exists('Channels'):
    os.mkdir('Channels')
os.chdir(os.path.join(os.getcwd(),'Channels'))
for i in groups:
    if not os.path.exists(i):
        os.mkdir(i)
    os.chdir(os.path.join(os.getcwd(),i))
    tel_df[tel_df['Name']==i].to_csv('0_'+i+'.csv', mode='w', index=False, header=False)
    os.chdir('C:\\Users\\Mohib\\Desktop\\Testing Channels\\Channels')

def extractor(i):
    i = str(i)
    suffixes = 'usdt|busd|futures'
    coinsregex = '|'.join(binance_coins)
    found = False
    text = re.sub(r'[^\w\s]', ' ', i)
    for s in text.split():
        if re.search("({})({})+|({})+({})|^({})$|[0-9]+({})|({})[0-9]+".format(coinsregex,suffixes,suffixes,coinsregex,coinsregex,coinsregex,coinsregex), s,re.IGNORECASE):
            found = True
            break
    if(found):
        return i
    else: return np.nan
tel_df['Cleaned Text'] = tel_df['Cleaned Text'].apply(extractor)
tel_df_fil1 = tel_df[tel_df['Cleaned Text'].notna()] 
tel_df_fil1

os.chdir('C:\\Users\\Mohib\\Desktop\\Testing Channels')
if not os.path.exists('Channels'):
    os.mkdir('Channels')
os.chdir(os.path.join(os.getcwd(),'Channels'))
for i in groups:
    if not os.path.exists(i):
        os.mkdir(i)
    os.chdir(os.path.join(os.getcwd(),i))
    tel_df_fil1[tel_df_fil1['Name']==i].to_csv('1_'+i+'.csv', mode='w', index=False, header=False)
    os.chdir('C:\\Users\\Mohib\\Desktop\\Testing Channels\\Channels')
os.chdir("C:\\Users\\Mohib\\Desktop\\FinalYear\\Telegram")
with open('datetime.txt', 'w') as f:
    f.write(str(datetime.now()))