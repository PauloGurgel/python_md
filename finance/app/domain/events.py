import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Event:
    correlation_id: str
    timestamp: datetime

    def __init__(self):
        self.correlation_id = str(uuid.uuid4())
        self.timestamp = datetime.now()


@dataclass
class FinanceAppointmentCreated(Event):
    appointment_id: str
    price: Decimal

    def __init__(self, appointment_id: str, price: Decimal):
        self.appointment_id = appointment_id
        self.correlation_id = str(uuid.uuid4())
        self.timestamp = datetime.now()
        self.price = price
        super().__init__()
