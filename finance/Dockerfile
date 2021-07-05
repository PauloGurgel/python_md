FROM ubuntu:latest

COPY . /var/www
WORKDIR /var/www

RUN apt-get clean \
    && apt-get -y update
RUN apt-get -y install python3.8 python3-pip python3.8-dev libssl-dev\
    && apt-get -y install build-essential libpq-dev librdkafka-dev wget tar

EXPOSE 5001

RUN python3 -m pip install -r requirements.txt --no-cache-dir
RUN chmod +x ./start.sh

CMD ["./start.sh"]
