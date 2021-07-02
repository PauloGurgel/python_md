from sqlalchemy import Table, MetaData, Column, Integer, Numeric
from sqlalchemy.orm import mapper

from app.domain.model import Appointment

metadata = MetaData()

appointments = Table(
    "appointments",
    metadata,
    Column("appointment_id", Integer, primary_key=True),
    Column("price", Numeric(precision=10, scale=2)),
)


def start_mappers():
    mapper(Appointment, appointments)
