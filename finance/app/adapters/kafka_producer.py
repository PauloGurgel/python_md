import json

from app import config, CustomJSONEncoder
from app.adapters import kafkaProducer
from app.domain.events import FinanceAppointmentCreated


def producing_log(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Kafka Message produced: %s" % (str(msg)))


def send_notification(event: FinanceAppointmentCreated):
    json_data = json.dumps(event, cls=CustomJSONEncoder)
    print("Send notification called for:" + json_data + " on topic: " + config.Config.APPOINTMENT_CREATED_EVENT_TOPIC)

    kafkaProducer.produce(topic=config.Config.APPOINTMENT_CREATED_EVENT_TOPIC,
                          key=event.appointment_id,
                          value=json_data,
                          callback=producing_log)
