import json

from app import config, CustomJSONEncoder
from app.adapters import kafkaProducer
from app.domain.events import ConsultationClosed


def producing_log(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


def send_notification(event: ConsultationClosed):
    json_data = json.dumps(event, cls=CustomJSONEncoder)
    print("Send notification called for:" + json_data + " on topic: " + config.Config.CONSULTATION_CLOSED_EVENT_TOPIC)

    kafkaProducer.produce(topic=config.Config.CONSULTATION_CLOSED_EVENT_TOPIC,
                          key=event.consultation_id,
                          value=json_data,
                          callback=producing_log)
