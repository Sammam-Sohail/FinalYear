import pymongo
import pandas as pd
from datetime import datetime
import os
client = pymongo.MongoClient(
    "mongodb://root:example@Mongo:27017/?authSource=admin&readPreference=primary&ssl=false&directConnection=true")
db = client.Twigram
print(os.getcwd())
df = pd.read_csv("./shared/Socker.csv")
df2 = df.groupby("Open Time")['Values'].apply(
    lambda x: '|'.join(x)).reset_index()
df2 = df2.sort_values(by=['Open Time'], ascending=False)
data_dict = df2.to_dict("records")
db.Binance.insert_many(data_dict)
print("Coins Data Inserted at", datetime.now())



for i in os.listdir("./shared/Calls/"):
    print(i)
    df = pd.read_pickle(f"./shared/Calls/{i}/2_{i}.pkl")
    df.drop(columns=["Cleaned_text"])
    data_dict = df.to_dict("records")
    db.Telegram.insert_many(data_dict)
    print("Signals Data Inserted at", datetime.now())

# with open('../shared/Last_Updated.txt', 'w') as f:
#     f.write(str(datetime.now()))

# str(datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
# db.Twigram_collection.deleteMany({Open Time: {"$lt": new Date(2017, 9, 1)}})


# ADD LAST UPDATED TIME TO ROOT FOLDER AND THEN PROCESS THE FOLLOWING
