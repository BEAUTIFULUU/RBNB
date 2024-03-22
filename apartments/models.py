import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from apartments.choices import COUNTRY_CHOICES, CURRENCY_CHOICES


class Address(models.Model):
    country = models.CharField(choices=COUNTRY_CHOICES)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=64)
    province = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=10)


class Apartment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    surface = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(3)]
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(1000)]
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    deposit = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(50)], null=True
    )
    is_available = models.BooleanField(default=True)
    description = models.CharField(max_length=600)
    is_furnished = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
