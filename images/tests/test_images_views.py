import os
import pytest
from _pytest.fixtures import SubRequest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apartments.models import Address, Apartment
from images.models import ApartmentImage

User = get_user_model()


@pytest.fixture
def authenticated_user() -> User:
    user = User.objects.create_user(username="testuser123", password="testpassword123")
    return user


@pytest.fixture
def authenticated_user_with_no_apartments() -> User:
    user = User.objects.create_user(
        username="testuser12345", password="testpassword54321"
    )
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


@pytest.fixture
def db_image(apartment: Apartment):
    test_image_path = os.path.join(
        os.path.dirname(__file__), "test_data", "valid_image.jpg"
    )
    image_obj = ApartmentImage.objects.create(
        image=test_image_path, apartment_id=apartment.id
    )
    return image_obj


@pytest.fixture
def in_memory_image(request: SubRequest):
    filename = request.param
    test_image_path = os.path.join(os.path.dirname(__file__), "test_data", filename)
    with open(test_image_path, "rb") as f:
        file_content = f.read()
        in_memory_file = SimpleUploadedFile(filename, file_content, "image/jpeg")
    return in_memory_file


@pytest.mark.django_db
class TestAdvertisementImageViewResponses:
    @pytest.mark.parametrize("in_memory_image", ["valid_image.jpg"], indirect=True)
    def test_advertisement_image_view_return_201_and_create_image_if_advertisement_owner_post_image(
        self,
        api_client: APIClient,
        in_memory_image: SimpleUploadedFile,
        apartment: Apartment,
    ):
        url = "upload_apartment_images"
        data = {"image": [in_memory_image]}

        response = api_client.post(
            reverse(url, kwargs={"advertisement_id": apartment.id}),
            data=data,
            format="multipart",
        )
        assert response.status_code == status.HTTP_201_CREATED
        expected_image_name = f"{in_memory_image.name}_adv_id: {apartment.id}.jpg"
        uploaded_image = ApartmentImage.objects.filter(
            apartment_id=apartment.id, image__icontains=expected_image_name
        )
        assert uploaded_image is not None

    @pytest.mark.parametrize("in_memory_image", ["valid_image.jpg"], indirect=True)
    def test_advertisement_image_view_return_403_for_anonymous_user(
        self, in_memory_image: SimpleUploadedFile, apartment: Apartment
    ):
        url = "upload_apartment_images"
        data = {"images": [in_memory_image]}
        client = APIClient()
        response = client.post(
            reverse(url, kwargs={"advertisement_id": apartment.id}),
            data=data,
            format="multipart",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert ApartmentImage.objects.filter(apartment_id=apartment.id).count() == 0

    @pytest.mark.parametrize("in_memory_image", ["valid_image.jpg"], indirect=True)
    def test_advertisement_image_view_return_403_for_user_which_is_not_owner(
        self,
        authenticated_user_with_no_apartments: User,
        apartment: Apartment,
        in_memory_image: SimpleUploadedFile,
    ):
        url = "upload_apartment_images"
        data = {"images": [in_memory_image]}
        client = APIClient()
        client.force_authenticate(user=authenticated_user_with_no_apartments)

        response = client.post(
            reverse(url, kwargs={"advertisement_id": apartment.id}),
            data=data,
            format="multipart",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert ApartmentImage.objects.filter(apartment_id=apartment.id).count() == 0


@pytest.mark.django_db
class TestAdvertisementImageDetailViewResponses:

    def test_advertisement_image_detail_view_return_200_and_apartment_image_obj_for_owner_user(
        self, api_client: APIClient, apartment: Apartment, db_image: ApartmentImage
    ):
        url = "get_advertisement_image_details"
        response = api_client.get(
            reverse(
                url, kwargs={"advertisement_id": apartment.id, "image_id": db_image.id}
            )
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(db_image.id)

    def test_advertisement_image_detail_view_return_403_for_user_which_is_not_apartment_owner(
        self,
        apartment: Apartment,
        db_image: ApartmentImage,
        authenticated_user_with_no_apartments: User,
    ):
        url = "get_advertisement_image_details"
        client = APIClient()
        client.force_authenticate(user=authenticated_user_with_no_apartments)
        response = client.get(
            reverse(
                url, kwargs={"advertisement_id": apartment.id, "image_id": db_image.id}
            )
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_advertisement_image_detail_view_return_403_for_anonymous_user(
        self, apartment: Apartment, db_image: ApartmentImage
    ):
        url = "get_advertisement_image_details"
        client = APIClient()
        response = client.get(
            reverse(
                url, kwargs={"advertisement_id": apartment.id, "image_id": db_image.id}
            )
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_advertisement_image_detail_view_return_200_and_update_apartment_image_obj_for_apartment_owner(
        self, api_client: APIClient, db_image: ApartmentImage, apartment: Apartment
    ):
        url = "get_advertisement_image_details"
        data = {"is_main": True}
        response = api_client.put(
            reverse(
                url, kwargs={"image_id": db_image.id, "advertisement_id": apartment.id}
            ),
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        updated_image = ApartmentImage.objects.get(id=db_image.id)
        assert updated_image.is_main is True
