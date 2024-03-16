import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apartments.models import Apartment, Address

User = get_user_model()


@pytest.fixture
def authenticated_user() -> User:
    user = User.objects.create_user(username="testuser123", password="testpassword123")
    return user


@pytest.fixture
def api_client(authenticated_user: User) -> APIClient:
    client = APIClient()
    client.force_login(authenticated_user)
    return client


@pytest.fixture
def address() -> Address:
    address_obj = Address.objects.create(
        street="teststreet",
        city="testcity",
        province="testprovince",
        postal_code="11-111",
        country="testcountry",
    )
    return address_obj


@pytest.fixture
def apartment(address: Address, authenticated_user: User) -> Apartment:
    apartment_obj = Apartment.objects.create(
        price="1000",
        deposit="500",
        is_available=True,
        description="description",
        address_id=address.id,
        owner_id=authenticated_user.id,
        is_furnished=True,
        surface="100",
    )
    return apartment_obj


@pytest.mark.django_db
class TestApartmentViewResponses:
    def test_apartment_view_return_403_for_anonymous_user(self):
        client = APIClient()
        url = "get_apartments"
        response = client.get(reverse(url))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_apartment_view_return_200_for_authenticated_user(
        self, api_client: APIClient
    ):
        url = "get_apartments"
        response = api_client.get(reverse(url))

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestApartmentDetailViewResponses:
    def test_apartment_detail_view_return_403_for_anonymous_user(
        self, apartment: Apartment
    ):
        client = APIClient()
        url = "get_apartment_details"
        response = client.get(reverse(url, kwargs={"apartment_id": apartment.id}))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_apartment_detail_view_return_200_for_authenticated_user(
        self, api_client: APIClient, apartment: Apartment
    ):
        url = "get_apartment_details"
        response = api_client.get(reverse(url, kwargs={"apartment_id": apartment.id}))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == apartment.id


@pytest.mark.django_db
class TestApartmentAdvertisementViewResponses:
    def test_apartment_advertisement_view_return_403_for_anonymous_user(self):
        client = APIClient()
        url = "get_owner_advertisements"
        response = client.get(reverse(url))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_apartment_advertisement_view_return_200_for_authenticated_user(
        self, api_client: APIClient
    ):
        url = "get_owner_advertisements"
        response = api_client.get(reverse(url))

        assert response.status_code == status.HTTP_200_OK

    def test_apartment_view_return_201_if_apartment_created(
        self, api_client: APIClient
    ):
        url = "get_owner_advertisements"
        data = {
            "surface": "100.00",
            "is_furnished": True,
            "price": "2000.00",
            "currency": "EUR",
            "deposit": "1000.00",
            "is_available": True,
            "description": "sadfadsdasdsa",
            "address": {
                "country": "Poland",
                "street": "teststreet",
                "city": "testcity",
                "province": "testprovince",
                "postal_code": "22-222",
            },
        }
        response = api_client.post(reverse(url), data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestApartmentAdvertisementDetailViewResponses:
    def test_apartment_detail_view_return_403_for_anonymous_user(
        self, apartment: Apartment
    ):
        client = APIClient()
        url = "get_owner_advertisement_details"
        response = client.get(reverse(url, kwargs={"advertisement_id": apartment.id}))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_apartment_detail_view_return_200_for_authenticated_user(
        self, apartment: Apartment, api_client: APIClient
    ):
        url = "get_owner_advertisement_details"
        response = api_client.get(
            reverse(url, kwargs={"advertisement_id": apartment.id})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == apartment.id

    def test_apartment_detail_view_return_200_if_apartment_updated_with_put_method(
        self, apartment: Apartment, api_client: APIClient
    ):
        url = "get_owner_advertisement_details"
        data = {
            "surface": "100.00",
            "is_furnished": True,
            "price": "2000.00",
            "currency": "EUR",
            "deposit": "1000.00",
            "is_available": True,
            "description": "sadfadsdasdsa",
            "address": {
                "country": "Poland",
                "street": "teststreet",
                "city": "testcity",
                "province": "testprovince",
                "postal_code": "22-222",
            },
        }
        response = api_client.put(
            reverse(url, kwargs={"advertisement_id": apartment.id}),
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_apartment_detail_view_return_200_if_apartment_updated_with_patch_method(
        self, apartment: Apartment, api_client: APIClient
    ):
        url = "get_owner_advertisement_details"
        data = {"deposit": "600", "address": {"street": "streettoo"}}
        result = api_client.patch(
            reverse(url, kwargs={"advertisement_id": apartment.id}),
            data=data,
            format="json",
        )

        assert result.status_code == status.HTTP_200_OK

    def test_apartment_detail_view_return_204_if_apartment_deleted(
        self, apartment: Apartment, api_client: APIClient
    ):
        url = "get_owner_advertisement_details"
        result = api_client.delete(
            reverse(url, kwargs={"advertisement_id": apartment.id})
        )

        assert result.status_code == status.HTTP_204_NO_CONTENT
