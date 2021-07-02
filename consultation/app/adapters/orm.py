from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import mapper

from app.domain.model import Consultation

metadata = MetaData()

consultations = Table(
    "consultations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("start_date", DateTime, nullable=False),
    Column("end_date", DateTime),
    Column("physician_id", String(255)),
    Column("patient_id", String(255)),
    Column("price", Numeric(precision=10, scale=2)),
)


def start_mappers():
    mapper(Consultation, consultations)
