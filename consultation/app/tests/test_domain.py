import datetime
from decimal import Decimal

from app.domain.events import ConsultationClosed
from app.tests import fake_factory


def test_domain_closing_based_on_model():
    end_date = datetime.datetime(2021, 6, 7, 16, 0, 0)
    consultation = fake_factory.create_base_consultation()
    consultation.close(end_date)
    assert consultation.price == Decimal(600)
    assert isinstance(consultation.events.pop(), ConsultationClosed)

