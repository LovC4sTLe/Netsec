FROM ubuntu:22.04

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y python3-pip

WORKDIR /apigateway

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . /apigateway

EXPOSE 5000

CMD ["python3", "app.py"]