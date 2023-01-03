FROM python:3.8-slim

WORKDIR /app/usr/src/

COPY . /app/usr/src/Binance_socket


RUN pip install -r ./Binance_socket/requirements.txt
RUN apt-get update & apt-get install

CMD [ "python","./Binance_socket/Binance_socket.py" ]
