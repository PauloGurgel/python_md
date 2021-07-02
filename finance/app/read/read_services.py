from typing import List

from app.adapters import orm
from app.domain.model import Appointment
from app.services.unit_of_work import AbstractUnitOfWork


def query_one_appointment(appointment_id, uow: AbstractUnitOfWork) -> Appointment:
    with uow:
        appointment_row = uow.session.query(orm.appointments).filter(
            orm.appointments.c.appointment_id == appointment_id).one()
        uow.commit()
        return Appointment(appointment_row['appointment_id'],
                           appointment_row['price'])


def query_all_appointments(uow: AbstractUnitOfWork) -> List:
    appointment_list = []
    with uow:
        appointments = list(uow.session.query(orm.appointments).all())
        for appointment_row in appointments:
            appointment_list.append(Appointment(appointment_row['appointment_id'],
                                                appointment_row['price']))

    return appointment_list
