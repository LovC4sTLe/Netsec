FROM ubuntu:22.04

RUN apt-get update -qq && apt-get install -y sqlite3 libpq-dev python3-pip

WORKDIR /authen-service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /authen-service

EXPOSE 5000

CMD ["python3", "app.py"]