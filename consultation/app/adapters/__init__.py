from confluent_kafka import Producer
import socket

from app import Config

conf = {'bootstrap.servers': Config.KAFKA_BROKER_URI,
        'client.id': 'iclinic_consultation_' + socket.gethostname()}

kafkaProducer = Producer(conf)
