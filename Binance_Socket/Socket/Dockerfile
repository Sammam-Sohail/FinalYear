FROM python:3.8-slim

WORKDIR /app/usr/src/

COPY . /app/usr/src/Socket


RUN pip install -r ./Socket/requirements.txt
RUN apt-get update & apt-get install

CMD [ "python","./Socket/Binance_socket.py" ]
