from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Apartment, Address


class AddressInputSerializer(serializers.Serializer):
    street = serializers.CharField(max_length=120)
    city = serializers.CharField(max_length=64)
    province = serializers.CharField(max_length=64)
    postal_code = serializers.CharField(max_length=10)


class AddressOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["street", "city", "province", "postal_code"]


class ApartmentInputSerializer(serializers.Serializer):
    surface = serializers.DecimalField(max_digits=5, decimal_places=2)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    deposit = serializers.DecimalField(max_digits=6, decimal_places=2)
    description = serializers.CharField(max_length=600)
    is_furnished = serializers.BooleanField(default=True)
    is_available = serializers.BooleanField(default=True)
    address = AddressInputSerializer()


class ApartmentOutputSerializer(serializers.ModelSerializer):
    address = AddressOutputSerializer()

    class Meta:
        model = Apartment
        fields = [
            "id",
            "surface",
            "is_furnished",
            "price",
            "deposit",
            "is_available",
            "address",
        ]


class ApartmentDetailOutputSerializer(serializers.ModelSerializer):
    address = AddressOutputSerializer()

    class Meta:
        model = Apartment
        fields = [
            "id",
            "surface",
            "is_furnished",
            "price",
            "deposit",
            "is_available",
            "description",
            "owner",
            "address",
        ]


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
