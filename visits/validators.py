import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from visits.models import Visit


def validate_create_apartment_visit(apartment_id: uuid.uuid4, user_id: int) -> None:
    if Visit.objects.filter(apartment_id=apartment_id, user_id=user_id).exists():
        raise ValidationError("Visit for this apartment already exists.")


def validate_apartment_visit_date(date_time: datetime) -> None:
    current_time = timezone.now()
    max_allowed_date = current_time + timedelta(days=60)

    if date_time < current_time:
        raise ValidationError("Visit date must be in the future.")

    if date_time > max_allowed_date:
        raise ValidationError(
            "Visit date cannot be more than 2 months from the current date."
        )
