FROM python:3.8-slim

WORKDIR /app/usr/src/

COPY Binance_socket.py /app/usr/src/
COPY requirements.txt /app/usr/src/
COPY config.cfg /app/usr/src/

# ADD https://dev.mysql.com/get/Downloads/Connector-ODBC/8.0/mysql-connector-odbc-8.0.26-linux-glibc2.12-x86-64bit.tar.gz .
# RUN tar -C . -xzvf mysql-connector-odbc-8.0.26-linux-glibc2.12-x86-64bit.tar.gz

RUN pip install -r requirements.txt
RUN apt-get update & apt-get install

CMD [ "python","Binance_socket.py" ]
