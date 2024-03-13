import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from apartments.models import Apartment


class ApartmentImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    image = models.ImageField(
        upload_to="images/",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"])],
    )
    is_main = models.BooleanField(default=False)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, null=True)
