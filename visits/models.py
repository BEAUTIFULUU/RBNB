import uuid

from django.contrib.auth.models import User
from django.db import models

from apartments.models import Apartment
from visits.choices import VISIT_STATES


class Visit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    state = models.CharField(choices=VISIT_STATES, default="PENDING")
