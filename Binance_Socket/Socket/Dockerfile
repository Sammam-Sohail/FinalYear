FROM python:3.8-slim

WORKDIR /app/usr/src/

COPY Binance_socket.py /app/usr/src/
COPY requirements.txt /app/usr/src/
COPY config.cfg /app/usr/src/


RUN pip install -r requirements.txt
RUN apt-get update & apt-get install

CMD [ "python","Binance_socket.py" ]
