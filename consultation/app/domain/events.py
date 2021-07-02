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
class ConsultationClosed(Event):
    consultation_id: str
    start_date: datetime
    end_date: datetime
    price: Decimal

    def __init__(self, consultation_id: str, start_date: datetime, end_date: datetime, price: Decimal):
        self.consultation_id = consultation_id
        self.correlation_id = str(uuid.uuid4())
        self.timestamp = datetime.now()
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        super().__init__()
