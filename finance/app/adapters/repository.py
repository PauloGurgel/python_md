import abc
from typing import Set

from app.domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Appointment]

    def add(self, appointment: model.Appointment):
        self._add(appointment)
        self.seen.add(appointment)

    def get(self, appointment_id) -> model.Appointment:
        appointment = self._get(appointment_id)
        if appointment:
            self.seen.add(appointment)
        return appointment

    @abc.abstractmethod
    def _add(self, appointment: model.Appointment):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, appointment_id) -> model.Appointment:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, appointment):
        self.session.add(appointment)

    def _get(self, appointment_id):
        return self.session.query(model.Appointment).filter_by(appointment_id=appointment_id).one()

    def list(self):
        return self.session.query(model.Appointment).all()
