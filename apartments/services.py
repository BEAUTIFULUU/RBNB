from django.shortcuts import get_object_or_404
from .models import Apartment, Address


def list_apartments() -> list[Apartment]:
    return Apartment.objects.all()


def get_apartment_details(apartment_id: int) -> Apartment:
    apartment_obj = Apartment.objects.filter(id=apartment_id)
    return get_object_or_404(apartment_obj)


def list_user_apartment_advertisements(user_id: int) -> list[Apartment]:
    return Apartment.objects.filter(owner_id=user_id)


def create_apartment_with_address(data: dict[str, any], owner_id: int) -> Apartment:
    address_data = data.pop("address")
    address_obj = Address.objects.create(**address_data)
    data["address"] = address_obj
    data["owner_id"] = owner_id
    apartment_obj = Apartment.objects.create(**data)
    return apartment_obj


def update_apartment_with_address(
    data: dict[str, any], apartment_obj: Apartment
) -> None:
    address_data = data.pop("address")
    update_apartment(apartment_obj, data)
    update_address(apartment_obj.address, address_data)


def update_apartment(apartment_obj: Apartment, data: dict[str, any]) -> None:
    for key, value in data.items():
        setattr(apartment_obj, key, value)
    apartment_obj.save()


def update_address(address_obj: Address, data: dict[str, any]) -> None:
    for key, value in data.items():
        setattr(address_obj, key, value)
    address_obj.save()
