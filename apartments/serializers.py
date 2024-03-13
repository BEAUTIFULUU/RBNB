from rest_framework import serializers

from apartments.choices import CURRENCY_CHOICES, COUNTRY_CHOICES
from apartments.models import Apartment, Address
from apartments.services import get_main_image_url
from images.serializers import ApartmentImageOutputSimpleSerializer


class AddressInputSerializer(serializers.Serializer):
    country = serializers.ChoiceField(choices=COUNTRY_CHOICES)
    street = serializers.CharField(max_length=120)
    city = serializers.CharField(max_length=64)
    province = serializers.CharField(max_length=64)
    postal_code = serializers.CharField(max_length=10)


class AddressOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["country", "street", "city", "province", "postal_code"]


class AddressSimpleOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["country", "province", "city"]


class ApartmentInputSerializer(serializers.Serializer):
    surface = serializers.DecimalField(max_digits=5, decimal_places=2)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    currency = serializers.ChoiceField(choices=CURRENCY_CHOICES)
    deposit = serializers.DecimalField(max_digits=6, decimal_places=2)
    description = serializers.CharField(max_length=600)
    is_furnished = serializers.BooleanField(default=True)
    is_available = serializers.BooleanField(default=True)
    address = AddressInputSerializer()


class ApartmentOutputSerializer(serializers.ModelSerializer):
    address = AddressSimpleOutputSerializer()
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Apartment
        fields = [
            "id",
            "surface",
            "is_furnished",
            "price",
            "currency",
            "main_image",
            "is_available",
            "address",
        ]

    def get_main_image(self, obj):
        return get_main_image_url(apartment_id=obj.id)


class ApartmentDetailOutputSerializer(serializers.ModelSerializer):
    address = AddressOutputSerializer()
    images = ApartmentImageOutputSimpleSerializer(many=True, source="apartmentimage_set", read_only=True)

    class Meta:
        model = Apartment
        fields = [
            "id",
            "surface",
            "is_furnished",
            "price",
            "currency",
            "deposit",
            "is_available",
            "description",
            "images",
            "owner",
            "address",
        ]
