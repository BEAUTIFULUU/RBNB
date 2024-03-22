import uuid
import datetime
from visits.models import Visit
from visits.validators import (
    validate_create_apartment_visit,
    validate_apartment_visit_date,
)


def create_apartment_visit(
    apartment_id: uuid.uuid4, user_id: int, date_time: datetime
) -> Visit:
    validate_create_apartment_visit(apartment_id=apartment_id, user_id=user_id)
    validate_apartment_visit_date(date_time=date_time)
    return Visit.objects.create(
        apartment_id=apartment_id, user_id=user_id, date_time=date_time
    )
