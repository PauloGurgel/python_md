import abc
from typing import Set

from app.domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Consultation]

    def add(self, consultation: model.Consultation):
        self._add(consultation)
        self.seen.add(consultation)

    def get(self, consultation_id) -> model.Consultation:
        consultation = self._get(consultation_id)
        if consultation:
            self.seen.add(consultation)
        return consultation

    @abc.abstractmethod
    def _add(self, consultation: model.Consultation):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, consultation_id) -> model.Consultation:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, consultation):
        self.session.add(consultation)

    def _get(self, consultation_id):
        return self.session.query(model.Consultation).filter_by(id=consultation_id).one()

    def list(self):
        return self.session.query(model.Consultation).all()
