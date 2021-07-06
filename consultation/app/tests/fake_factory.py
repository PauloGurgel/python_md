from datetime import datetime
from decimal import Decimal

from app.domain.model import Consultation


def create_base_consultation():
    start_date = datetime(2021, 6, 7, 13, 0, 0)
    return Consultation(id='2139cf31-2625-43af-a6f2-987f8b8b5608',
                        start_date=start_date,
                        end_date=None,
                        patient_id='72711c79-6d4e-47b9-83f7-34e02d45c5a4',
                        physician_id='8c3248d4-1274-4cbe-92d7-af2ea1fccbed',
                        price=Decimal(0))
