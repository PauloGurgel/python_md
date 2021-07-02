from typing import List, Dict, Callable, Type

from app.adapters import kafka_producer
from app.domain import events


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


def send_finance_appointment_created_event(event: events.FinanceAppointmentCreated):
    kafka_producer.send_notification(event)


HANDLERS = {
    events.FinanceAppointmentCreated: [send_finance_appointment_created_event],
}  # type: Dict[Type[events.Event], List[Callable]]
