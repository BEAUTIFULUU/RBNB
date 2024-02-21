from django.shortcuts import get_object_or_404
from .models import Apartment, Address


def list_apartments() -> list[Apartment]:
    return Apartment.objects.all()


def get_apartment_details(apartment_id: int) -> Apartment:
    apartment_obj = Apartment.objects.filter(id=apartment_id)
    return get_object_or_404(apartment_obj)
