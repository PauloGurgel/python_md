import uuid
from datetime import datetime
from decimal import Decimal

from app.domain import model
from app.services import unit_of_work


def create_new_consultation(
    start_date: datetime, physician_id: str, patient_id: str,
    uow: unit_of_work.AbstractUnitOfWork
) -> str:
    base_price = Decimal(0)
    consulting_id = str(uuid.uuid4())
    with uow:
        uow.consultations.add(model.Consultation(consulting_id,
                                                 start_date=start_date,
                                                 end_date=None,
                                                 physician_id=physician_id,
                                                 patient_id=patient_id,
                                                 price=base_price))
        uow.commit()

    return consulting_id


def close_consultation(consultation_id: str, end_date: datetime, uow: unit_of_work.AbstractUnitOfWork) -> str:
    with uow:
        consultation = uow.consultations.get(consultation_id)
        consultation.close(end_date=end_date)
        uow.consultations.add(consultation)
        uow.commit()
        return consultation
