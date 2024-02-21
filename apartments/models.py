from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(100)]
    )
    deposit = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(50)], null=True
    )
    surface = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(3)]
    )
    description = models.CharField(max_length=600, null=True)
    is_furnished = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    tenants = models.ManyToManyField(User, related_name="rooms")


class Address(models.Model):
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=64)
    province = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=10, unique=True)


class Preferences(models.Model):
    price = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(100)]
    )
    surface = models.DecimalField(
        max_digits=3, decimal_places=2, validators=[MinValueValidator(3)]
    )
    is_furnished = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Apartment(models.Model):
    surface = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(3)], default=0.00
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(1000)]
    )
    deposit = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(50)], null=True
    )
    is_available = models.BooleanField(default=True)
    description = models.CharField(max_length=600)
    is_furnished = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)


class Visit(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=False, auto_now=False)
