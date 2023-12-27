FROM ubuntu:22.04

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 libsqlite3-dev 
RUN apt-get install -y python3-pip

WORKDIR /authen-service

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . /authen-service

EXPOSE 5000

CMD ["python3", "app.py"]