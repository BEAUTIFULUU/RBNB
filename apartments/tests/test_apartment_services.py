from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.http import Http404

from apartments.models import Apartment, Address
from apartments.services import (
    list_apartments,
    get_apartment_details,
    list_owner_apartment_advertisements,
    create_apartment_with_address,
    update_apartment,
    update_address,
    update_apartment_with_address,
)

User = get_user_model()


@pytest.fixture
def create_user():
    user = User.objects.create(username="testuser123", password="testpassword123")
    return user


@pytest.fixture
def create_address_obj():
    address_obj = Address.objects.create(
        street="teststreet",
        city="testcity",
        province="testprovince",
        postal_code="11-111",
        country="testcountry",
    )
    return address_obj


@pytest.fixture
def create_apartment_obj(create_address_obj, create_user):
    user = create_user
    address_obj = create_address_obj
    apartment_obj = Apartment.objects.create(
        price="1000",
        deposit="500",
        is_available=True,
        description="description",
        address_id=address_obj.id,
        owner_id=user.id,
        is_furnished=True,
        surface="100",
    )
    return apartment_obj


@pytest.mark.django_db
class TestApartmentServices:
    def test_list_apartments_return_apartments_if_apartment_exists(
        self, create_apartment_obj
    ):
        apartment_obj = create_apartment_obj
        apartments = list_apartments()

        assert len(apartments) == 1
        assert apartment_obj in apartments

    def test_get_apartment_details_return_apartment_obj_if_apartment_exists(
        self, create_apartment_obj
    ):
        apartment_obj = create_apartment_obj
        apartment_details = get_apartment_details(apartment_id=apartment_obj.id)

        assert apartment_obj == apartment_details

    def test_get_apartment_details_return_404_if_apartment_does_not_exist(self):
        with pytest.raises(Http404):
            get_apartment_details(apartment_id=9999)

    def test_list_owner_apartment_advertisements_return_user_apartments_if_apartments_exists(
        self, create_apartment_obj
    ):
        apartment_obj = create_apartment_obj
        apartments_adv = list_owner_apartment_advertisements(
            user_id=apartment_obj.owner_id
        )

        assert len(apartments_adv) == 1
        assert apartment_obj in apartments_adv

    def test_create_apartment_with_address_create_apartment_obj_if_data_is_valid(
        self, create_user
    ):
        user = create_user
        data = {
            "surface": "100.00",
            "is_furnished": True,
            "price": "2000.00",
            "deposit": "1000.00",
            "is_available": True,
            "address": {
                "country": "testcountry",
                "street": "teststreet",
                "city": "testcity",
                "province": "testprovince",
                "postal_code": "22-222",
            },
        }
        assert Apartment.objects.count() == 0
        created_apartment = create_apartment_with_address(data=data, owner_id=user.id)
        assert Apartment.objects.count() == 1
        owner_apartments = Apartment.objects.filter(owner_id=user.id)
        assert created_apartment in owner_apartments

    def test_update_address_update_address_obj_if_data_is_valid(
        self, create_address_obj
    ):
        address_obj = create_address_obj
        data = {
            "street": "new_street",
            "city": "new_city",
            "province": "new_province",
            "postal_code": "11-222",
            "country": "new_country",
        }
        update_address(address_obj, data)
        updated_address = Address.objects.get(id=address_obj.id)
        assert updated_address.street == data["street"]
        assert updated_address.city == data["city"]
        assert updated_address.province == data["province"]
        assert updated_address.postal_code == data["postal_code"]
        assert updated_address.country == data["country"]

    def test_update_apartment_update_apartment_obj_if_data_is_valid(
        self, create_apartment_obj
    ):
        apartment_obj = create_apartment_obj
        data = {
            "surface": "150.00",
            "is_furnished": True,
            "price": "4000.00",
            "deposit": "2000.00",
            "is_available": True,
        }
        update_apartment(apartment_obj, data)
        updated_apartment = Apartment.objects.get(id=apartment_obj.id)
        assert updated_apartment.surface == Decimal("150.00")
        assert updated_apartment.is_furnished is True
        assert updated_apartment.price == Decimal("4000.00")
        assert updated_apartment.deposit == Decimal("2000.00")
        assert updated_apartment.is_available is True

    def test_update_apartment_with_address_update_apartment_if_data_is_valid(
        self, create_apartment_obj
    ):
        apartment_obj = create_apartment_obj
        data = {
            "surface": "150.00",
            "is_furnished": False,
            "price": "8000.00",
            "deposit": "4000.00",
            "is_available": True,
            "address": {
                "country": "updcountry",
                "street": "updstreet",
                "city": "updcity",
                "province": "updprovince",
                "postal_code": "55-555",
            },
        }
        update_apartment_with_address(data=data, apartment_obj=apartment_obj)
        updated_apartment_obj = Apartment.objects.get(id=apartment_obj.id)

        updated_apartment_data = {
            "surface": Decimal("150.00"),
            "is_furnished": False,
            "price": Decimal("8000.00"),
            "deposit": Decimal("4000.00"),
            "is_available": True,
        }
        for key, value in updated_apartment_data.items():
            assert getattr(updated_apartment_obj, key) == value

        updated_address_data = {
            "country": "updcountry",
            "street": "updstreet",
            "city": "updcity",
            "province": "updprovince",
            "postal_code": "55-555",
        }
        for key, value in updated_address_data.items():
            assert getattr(updated_apartment_obj.address, key) == value
