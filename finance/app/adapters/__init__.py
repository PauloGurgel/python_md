from confluent_kafka import Producer
import socket

from app import Config

kafka_config = {'bootstrap.servers': Config.KAFKA_BROKER_URI,
                'client.id': 'iclinic_finance_' + socket.gethostname()}

print(f'Producer configuration: {kafka_config}')
kafkaProducer = Producer(kafka_config)
