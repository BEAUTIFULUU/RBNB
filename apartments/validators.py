from rest_framework import serializers

from apartments.models import Address


def validate_postal_code(value):
    if Address.objects.filter(postal_code=value).exists():
        raise serializers.ValidationError("Postal code must be unique.")
    return value
