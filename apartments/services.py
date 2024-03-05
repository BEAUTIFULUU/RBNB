from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from .models import Apartment, Address


def list_apartments() -> QuerySet[Apartment]:
    return Apartment.objects.all()


def get_apartment_details(apartment_id: int) -> Apartment:
    apartment_obj = Apartment.objects.filter(id=apartment_id).select_related("address")
    return get_object_or_404(apartment_obj)


def list_owner_apartments(owner: int) -> QuerySet[Apartment]:
    return Apartment.objects.filter(owner_id=owner).select_related("address")


def create_apartment_with_address(data: dict[str, any], owner: int) -> Apartment:
    address_data = data.pop("address")
    address_obj = Address.objects.create(**address_data)
    data["address"] = address_obj
    data["owner_id"] = owner
    apartment_obj = Apartment.objects.create(**data)
    return apartment_obj


def update_apartment_with_address(
    data: dict[str, any], apartment_obj: Apartment
) -> None:
    if "address" in data:
        address_data = data.pop("address")
        _update_apartment_data(apartment_obj.address, address_data)

    _update_apartment_data(apartment_obj, data)


def _update_apartment_data(obj: Apartment | Address, data: dict[str, any]) -> None:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.save()
