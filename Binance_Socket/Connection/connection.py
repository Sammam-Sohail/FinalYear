import pymongo
import pandas as pd
from datetime import datetime
client = pymongo.MongoClient(
    "mongodb://root:example@Mongo:27017/?authSource=admin&readPreference=primary&ssl=false&directConnection=true")
db = client.Twigram
df = pd.read_csv("./shared/Socker.csv")
df2 = df.groupby("Open Time")['Values'].apply(
    lambda x: '|'.join(x)).reset_index()
df2 = df2.sort_values(by=['Open Time'], ascending=False)
data_dict = df2.to_dict("records")
db.Twigram_collection.insert_many(data_dict)
print("Data Inserted at", datetime.now())

# str(datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
# db.Twigram_collection.deleteMany({Open Time: {"$lt": new Date(2017, 9, 1)}})


# ADD LAST UPDATED TIME TO ROOT FOLDER AND THEN PROCESS THE FOLLOWING
