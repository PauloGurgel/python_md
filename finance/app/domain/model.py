from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import List

from . import events


@dataclass(unsafe_hash=True)
class Appointment:
    appointment_id: str
    price: Decimal

    events = []  # type: List[events.Event]
