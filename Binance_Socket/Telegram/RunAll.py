import os
Channels = ["BitmexCourses","CryptoClassicsVIP"]
for i in Channels:
    os.system(f'python ./Telegram/Channels/{i}/{i}.py')
