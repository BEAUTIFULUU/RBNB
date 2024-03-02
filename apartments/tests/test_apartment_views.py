import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apartments.models import Apartment, Address

User = get_user_model()


@pytest.fixture
def create_authenticated_user():
    user = User.objects.create_user(username="testuser123", password="testpassword123")
    client = APIClient()
    client.login(username="testuser123", password="testpassword123")
    return user, client


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
def create_apartment_obj(create_address_obj, create_authenticated_user):
    user, _ = create_authenticated_user
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
class TestApartmentAdvertiseViewResponses:
    def test_apartment_advertise_view_return_403_for_anonymous_user(self):
        client = APIClient()
        url = "get_apartment_adv"
        response = client.get(reverse(url))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_apartment_advertise_view_return_200_for_authenticated_user(
        self, create_authenticated_user
    ):
        user, client = create_authenticated_user
        url = "get_apartment_adv"
        response = client.get(reverse(url))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestApartmentAdvertiseDetailViewResponses:
    def test_apartment_advertise_detail_view_return_403_for_anonymous_user(
        self, create_apartment_obj
    ):
        apartment_obj = create_apartment_obj
        client = APIClient()
        url = "get_apartment_adv_details"
        response = client.get(reverse(url, kwargs={"apartment_id": apartment_obj.id}))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_apartment_advertise_detail_view_return_200_for_authenticated_user(
        self, create_authenticated_user, create_apartment_obj
    ):
        apartment_obj = create_apartment_obj
        user, client = create_authenticated_user
        url = "get_apartment_adv_details"
        response = client.get(reverse(url, kwargs={"apartment_id": apartment_obj.id}))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestApartmentViewResponses:
    def test_apartment_view_return_403_for_anonymous_user(self):
        client = APIClient()
        url = "get_create_owner_apartments"
        response = client.get(reverse(url))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_apartment_view_return_200_for_authenticated_user(
        self, create_authenticated_user
    ):
        user, client = create_authenticated_user
        url = "get_create_owner_apartments"
        response = client.get(reverse(url))

        assert response.status_code == status.HTTP_200_OK

    def test_apartment_view_return_201_if_apartment_created(
        self, create_authenticated_user
    ):
        user, client = create_authenticated_user
        url = "get_create_owner_apartments"
        data = {
            "surface": "123.00",
            "is_furnished": True,
            "price": "3333.00",
            "deposit": "444.00",
            "is_available": False,
            "description": "aaa",
            "address": {
                "country": "fdgsa",
                "street": "gdsa",
                "city": "asdgf",
                "province": "gdsa",
                "postal_code": "44-777",
            },
        }
        response = client.post(reverse(url), data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestApartmentDetailViewResponses:
    def test_apartment_detail_view_return_403_for_anonymous_user(
        self, create_apartment_obj
    ):
        apartment_obj = create_apartment_obj
        client = APIClient()
        url = "get_update_delete_owner_apartment"
        response = client.get(reverse(url, kwargs={"apartment_id": apartment_obj.id}))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_apartment_detail_view_return_200_for_authenticated_user(
        self, create_apartment_obj, create_authenticated_user
    ):
        apartment_obj = create_apartment_obj
        user, client = create_authenticated_user
        url = "get_update_delete_owner_apartment"
        response = client.get(reverse(url, kwargs={"apartment_id": apartment_obj.id}))

        assert response.status_code == status.HTTP_200_OK

    def test_apartment_detail_view_return_200_if_apartment_updated_with_put_method(
        self, create_apartment_obj, create_authenticated_user
    ):
        apartment_obj = create_apartment_obj
        user, client = create_authenticated_user
        url = "get_update_delete_owner_apartment"
        data = {
            "surface": "555.00",
            "is_furnished": True,
            "price": "9999.99",
            "deposit": "8888.88",
            "is_available": False,
            "description": "fsdafsad",
            "address": {
                "country": "fggsgs",
                "street": "asdf",
                "city": "gfds",
                "province": "asdf",
                "postal_code": "99-111",
            },
        }
        response = client.put(
            reverse(url, kwargs={"apartment_id": apartment_obj.id}),
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_apartment_detail_view_return_200_if_apartment_updated_with_patch_method(
        self, create_apartment_obj, create_authenticated_user
    ):
        apartment_obj = create_apartment_obj
        user, client = create_authenticated_user
        url = "get_update_delete_owner_apartment"
        data = {"deposit": "600", "address": {"street": "streettoo"}}
        result = client.patch(
            reverse(url, kwargs={"apartment_id": apartment_obj.id}),
            data=data,
            format="json",
        )

        assert result.status_code == status.HTTP_200_OK

    def test_apartment_detail_view_return_204_if_apartment_deleted(
        self, create_apartment_obj, create_authenticated_user
    ):
        apartment_obj = create_apartment_obj
        user, client = create_authenticated_user
        url = "get_update_delete_owner_apartment"
        result = client.delete(reverse(url, kwargs={"apartment_id": apartment_obj.id}))

        assert result.status_code == status.HTTP_204_NO_CONTENT
