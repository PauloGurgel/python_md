import logging
from decimal import Decimal

from app.domain import model
from app.services import unit_of_work


logger = logging.getLogger('iclinic_finance')


def create_new_appointment(appointment_id: str,
                           price: Decimal,
                           uow: unit_of_work.AbstractUnitOfWork) -> str:

    with uow:
        appointment = uow.appointments.get(appointment_id=appointment_id)
        logger.info(f"Found appointment: {appointment}")

        if appointment is None:  # Idempotency check
            uow.appointments.add(model.Appointment(appointment_id=appointment_id, price=price))

        uow.commit()

    return appointment_id
