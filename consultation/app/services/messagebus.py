from typing import List, Dict, Callable, Type

from app.adapters import kafka_producer
from app.domain import events


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


def send_consultation_closed_event(event: events.ConsultationClosed):
    kafka_producer.send_notification(event)


HANDLERS = {
    events.ConsultationClosed: [send_consultation_closed_event],
}  # type: Dict[Type[events.Event], List[Callable]]
