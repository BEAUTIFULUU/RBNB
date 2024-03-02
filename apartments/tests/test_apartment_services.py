from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.http import Http404

from apartments.models import Apartment, Address
from apartments.services import (
    list_apartments,
    get_apartment_details,
    list_owner_apartments,
    create_apartment_with_address,
    _update_apartment_data,
    update_apartment_with_address,
)

User = get_user_model()


@pytest.fixture
def user():
    user = User.objects.create(username="testuser123", password="testpassword123")
    return user


@pytest.fixture
def address():
    address_obj = Address.objects.create(
        street="teststreet",
        city="testcity",
        province="testprovince",
        postal_code="11-111",
        country="Poland",
    )
    return address_obj


@pytest.fixture
def apartment(address, user):
    apartment_obj = Apartment.objects.create(
        surface="100",
        is_furnished=True,
        price="1000",
        currency="EUR",
        deposit="500",
        description="description",
        is_available=True,
        address_id=address.id,
        owner_id=user.id,
    )
    return apartment_obj


@pytest.mark.django_db
class TestApartmentServices:
    def test_list_apartments_return_apartments_if_apartment_exists(self, apartment):
        apartments = list_apartments()

        assert len(apartments) == 1
        assert apartment in apartments

    def test_get_apartment_details_return_apartment_obj_if_apartment_exists(
        self, apartment
    ):
        apartment_details = get_apartment_details(apartment_id=apartment.id)

        assert apartment == apartment_details

    def test_get_apartment_details_return_404_if_apartment_does_not_exist(self):
        with pytest.raises(Http404):
            get_apartment_details(apartment_id=9999)

    def test_list_owner_apartment_advertisements_return_user_apartments_if_apartments_exists(
        self, apartment
    ):
        apartments_adv = list_owner_apartments(owner=apartment.owner_id)

        assert len(apartments_adv) == 1
        assert apartment in apartments_adv

    def test_create_apartment_with_address_create_apartment_obj_if_data_is_valid(
        self, user
    ):
        data = {
            "surface": "100.00",
            "is_furnished": True,
            "price": "2000.00",
            "currency": "EUR",
            "deposit": "1000.00",
            "is_available": True,
            "address": {
                "country": "Poland",
                "street": "teststreet",
                "city": "testcity",
                "province": "testprovince",
                "postal_code": "22-222",
            },
        }
        assert Apartment.objects.count() == 0
        created_apartment = create_apartment_with_address(data=data, owner=user.id)
        assert Apartment.objects.count() == 1
        owner_apartments = Apartment.objects.filter(owner_id=user.id)
        assert created_apartment in owner_apartments

    def test__update_apartment_data_update_apartment_if_data_is_valid(self, apartment):
        data = {
            "surface": Decimal("150.00"),
            "is_furnished": False,
            "price": Decimal("8000.00"),
            "currency": "USD",
            "deposit": Decimal("4000.00"),
            "description": "updateddescription",
            "is_available": True,
            "address": apartment.address,
        }

        _update_apartment_data(data=data, obj=apartment)
        updated_apartment = Apartment.objects.values().get(id=apartment.id)
        data.pop("address", None)
        updated_apartment.pop("address_id", None)
        updated_apartment.pop("id", None)
        updated_apartment.pop("owner_id", None)
        assert updated_apartment == data

    def test_update_apartment_with_address_update_apartment_if_data_is_valid(
        self, apartment
    ):
        data = {
            "surface": Decimal("150.00"),
            "is_furnished": False,
            "price": Decimal("8000.00"),
            "description": "upddescription",
            "currency": "USD",
            "deposit": Decimal("4000.00"),
            "is_available": True,
            "address": {
                "country": "updcountry",
                "street": "updstreet",
                "city": "updcity",
                "province": "updprovince",
                "postal_code": "55-555",
            },
        }
        update_apartment_with_address(data=data, apartment_obj=apartment)
        updated_apartment_data = Apartment.objects.values().get(id=apartment.id)
        updated_apartment_data.pop("address_id", None)
        updated_apartment_data.pop("id")
        updated_apartment_data.pop("owner_id")
        assert updated_apartment_data == data
