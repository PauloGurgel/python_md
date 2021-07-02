from __future__ import annotations

import datetime
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List
from . import events
from ..utils import date_utils


_BASE_PRICE = 200.0


@dataclass(unsafe_hash=True)
class Consultation:
    id: str
    start_date: datetime.datetime
    end_date: Optional[datetime.datetime]
    physician_id: str
    patient_id: str
    price: Decimal

    events = []  # type: List[events.Event]

    def close(self, end_date):
        self.end_date = end_date
        hours = date_utils.hours_between(end_date, self.start_date)
        self.price = Decimal(hours * _BASE_PRICE)

        self.events.append(events.ConsultationClosed(consultation_id=self.id,
                                                     start_date=self.start_date,
                                                     end_date=self.end_date,
                                                     price=self.price))
