from typing import List

from app.adapters import orm
from app.domain.model import Consultation
from app.services.unit_of_work import AbstractUnitOfWork


def query_one_consultation(consultation_id, uow: AbstractUnitOfWork) -> Consultation:
    with uow:
        consultation_row = uow.session.query(orm.consultations).filter(orm.consultations.c.id == consultation_id).one()
        uow.commit()
        return Consultation(consultation_row['id'],
                            consultation_row['start_date'],
                            consultation_row['end_date'],
                            consultation_row['physician_id'],
                            consultation_row['patient_id'],
                            consultation_row['price'])


def query_all_consultations(uow: AbstractUnitOfWork) -> List:
    consultation_list = []
    with uow:
        consultations = list(uow.session.query(orm.consultations).all())
        for consultation_row in consultations:
            consultation_list.append(Consultation(consultation_row['id'],
                                                  consultation_row['start_date'],
                                                  consultation_row['end_date'],
                                                  consultation_row['physician_id'],
                                                  consultation_row['patient_id'],
                                                  consultation_row['price']))

    return consultation_list
