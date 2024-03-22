from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from apartments.models import Apartment, Address
from images.models import ApartmentImage


def list_apartments() -> QuerySet:
    return Apartment.objects.filter(is_available=True)


def get_apartment_details(apartment_id: int) -> Apartment:
    apartment_obj = Apartment.objects.filter(id=apartment_id).select_related("address")
    return get_object_or_404(apartment_obj)


def get_apartment_advertisement_details(apartment_id: int, owner_id: int) -> Apartment:
    apartment_obj = Apartment.objects.filter(
        id=apartment_id, owner_id=owner_id
    ).select_related("address")
    return get_object_or_404(apartment_obj)


def list_owner_apartments(owner_id: int) -> QuerySet:
    return Apartment.objects.filter(owner_id=owner_id).select_related("address")


def create_apartment(data: dict[str, any], owner: int) -> Apartment:
    address_data = data.pop("address")
    address_obj = Address.objects.create(**address_data)
    data["address"] = address_obj
    data["owner_id"] = owner
    apartment_obj = Apartment.objects.create(**data)
    return apartment_obj


def update_apartment(data: dict[str, any], apartment_obj: Apartment) -> None:
    if "address" in data:
        address_data = data.pop("address")
        _update_apartment_data(apartment_obj.address, address_data)

    _update_apartment_data(apartment_obj, data)


def _update_apartment_data(obj: Apartment | Address, data: dict[str, any]) -> None:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.save()


def get_main_image_url(apartment_id: int) -> str | None:
    main_image_instance = ApartmentImage.objects.filter(
        apartment_id=apartment_id, is_main=True
    ).first()
    if main_image_instance:
        return main_image_instance.image.url
    return None
