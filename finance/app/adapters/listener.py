import json
import logging
import sys
import threading
from decimal import Decimal
from types import SimpleNamespace

from confluent_kafka import Consumer, KafkaException, KafkaError
from app import Config
from app.services import services, unit_of_work


logger = logging.getLogger('iclinic_finance')


def commit_completed(err, partitions):
    if err:
        logger.info(str(err))
    else:
        logger.info("Committed partition offsets: " + str(partitions))


kafka_config = {'bootstrap.servers': Config.KAFKA_BROKER_URI,
                'group.id': "iclinic_finance",
                'auto.offset.reset': 'smallest',
                'on_commit': commit_completed}
logger.info(f"Consumer config: {kafka_config}")
kafka_consumer = Consumer(kafka_config)
running = True


def msg_process(msg):
    try:
        msg_key = msg.key()
        msg_value = msg.value()
        logger.info(f"Received {msg_key}: {msg_value} from Kafka")
        data = json.loads(msg_value, object_hook=lambda d: SimpleNamespace(**d))
        services.create_new_appointment(data.consultation_id, Decimal(data.price), unit_of_work.SqlAlchemyUnitOfWork())
    except AttributeError:
        logger.info("Invalid message on topic. It will be ignored")


def consume_loop(consumer, topics):
    logger.info("Started consumer loop")
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=2.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                kafka_consumer.commit(asynchronous=False)
                msg_process(msg)

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def run_kafka_listener():
    logger.info("Starting kafka listener")
    topics = [Config.CONSULTATION_CLOSED_EVENT_TOPIC]
    th = threading.Thread(target=consume_loop(kafka_consumer, topics))
    # Start the thread
    th.start()
