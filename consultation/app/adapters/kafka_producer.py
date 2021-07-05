import json
import logging

from app import config, CustomJSONEncoder
from app.adapters import kafkaProducer
from app.domain.events import ConsultationClosed


logger = logging.getLogger('iclinic_consultation')


def producing_log(err, msg):
    if err is not None:
        logger.info("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        logger.info("Message produced: %s" % (str(msg)))


def send_notification(event: ConsultationClosed):
    json_data = json.dumps(event, cls=CustomJSONEncoder)
    logger.info(
        f"{event.correlation_id}: Sending notification called for: {json_data} on topic: {config.Config.CONSULTATION_CLOSED_EVENT_TOPIC}")

    kafkaProducer.poll(0)
    logger.debug(f"{event.correlation_id}: pooled")
    kafkaProducer.produce(topic=config.Config.CONSULTATION_CLOSED_EVENT_TOPIC,
                          key=event.consultation_id,
                          value=json_data,
                          callback=producing_log)
    logger.debug(f"{event.correlation_id}: produced")
    kafkaProducer.flush()

    logger.info(f"{event.correlation_id}: Notification flushed")
