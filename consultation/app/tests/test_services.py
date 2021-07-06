import datetime
from decimal import Decimal

from app.adapters import repository
from app.services import unit_of_work, services
from app.tests import fake_factory


class FakeRepository(repository.AbstractRepository):
    def __init__(self, consultations):
        super().__init__()
        self._consultations = set(consultations)

    def _add(self, consultation):
        self._consultations.clear()
        self._consultations.add(consultation)

    def _get(self, consultation_id):
        return next((p for p in self._consultations if p.id == consultation_id), None)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.consultations = FakeRepository([])
        self.committed = False

    def _commit(self):
        self.committed = True

    def _handle(self, event):
        print("Event handled")

    def rollback(self):
        # not tested yet
        pass


def test_close_consultation():
    uow = FakeUnitOfWork()
    consultation = fake_factory.create_base_consultation()
    hours_added = datetime.timedelta(hours=4)
    end_date = consultation.start_date + hours_added

    uow.consultations.add(consultation)
    services.close_consultation(consultation.id, end_date=end_date, uow=uow)

    assert consultation is not None
    assert consultation.price == Decimal(800)
    assert uow.committed


def test_create_consultation():
    uow = FakeUnitOfWork()
    start_date = datetime.datetime(2021, 6, 7, 14, 26, 0)
    patient_id = '92c1de13-bb9b-404e-a183-3533be74985a'
    physician_id = 'bad7e735-65ef-4d80-83b7-9de926041d31'
    id = services.create_new_consultation(start_date=start_date,
                                     physician_id=physician_id,
                                     patient_id=patient_id,
                                     uow=uow)

    consultation = uow.consultations.get(id)
    assert id != ''
    assert consultation.physician_id == physician_id
    assert uow.committed
