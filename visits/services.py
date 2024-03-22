import uuid
import datetime
from django.db.models import QuerySet
from visits.models import Visit
from visits.validators import (
    validate_create_apartment_visit,
)


def create_apartment_visit(
    apartment_id: uuid.uuid4, user_id: int, date_time: datetime
) -> Visit:
    validate_create_apartment_visit(apartment_id=apartment_id, user_id=user_id)
    return Visit.objects.create(
        apartment_id=apartment_id, user_id=user_id, date_time=date_time
    )


def get_owner_apartments_visits(owner_id: int) -> QuerySet:
    return Visit.objects.filter(apartment__owner=owner_id)


def get_tenant_apartments_visits(tenant_id: int) -> QuerySet:
    return Visit.objects.filter(user_id=tenant_id)
