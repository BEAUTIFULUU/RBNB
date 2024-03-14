import os
import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from apartments.models import Address, Apartment
from images.models import ApartmentImage
from images.services import (
    create_apartment_image_obj,
    get_apartment_image_details,
    delete_apartment_image_obj,
    _get_main_image,
    update_apartment_image_obj,
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


@pytest.fixture
def db_image(apartment):
    test_image_path = os.path.join(
        os.path.dirname(__file__), "test_data", "valid_image.jpg"
    )
    image_obj = ApartmentImage.objects.create(
        image=test_image_path, apartment_id=apartment.id
    )
    return image_obj


@pytest.fixture
def db_image_main(apartment):
    test_image_path = os.path.join(
        os.path.dirname(__file__), "test_data", "valid_image.jpg"
    )
    image_obj = ApartmentImage.objects.create(
        image=test_image_path, apartment_id=apartment.id, is_main=True
    )
    return image_obj


@pytest.fixture
def in_memory_image(request):
    filename = request.param
    test_image_path = os.path.join(os.path.dirname(__file__), "test_data", filename)
    with open(test_image_path, "rb") as f:
        file_content = f.read()
        in_memory_file = SimpleUploadedFile(filename, file_content, "image/jpeg")
    return in_memory_file


@pytest.mark.django_db
class TestImagesServices:
    @pytest.mark.parametrize("in_memory_image", ["valid_image.jpg"], indirect=True)
    def test_create_image_obj_creates_image_if_image_is_valid(
        self, in_memory_image, apartment
    ):
        assert ApartmentImage.objects.count() == 0
        created_apartment_image = create_apartment_image_obj(
            image=in_memory_image, advertisement_id=apartment.id
        )
        assert ApartmentImage.objects.count() == 1
        os.remove(f"images/{created_apartment_image.image.name}")

    def test_get_image_details_return_apartment_image_obj(self, db_image):
        apartment_image_obj = get_apartment_image_details(
            image_id=db_image.id, apartment_id=db_image.apartment_id
        )
        assert apartment_image_obj is not None
        assert apartment_image_obj.id == db_image.id
        assert apartment_image_obj.apartment_id == db_image.apartment_id

    def test_delete_apartment_image_obj_deletes_obj(self, db_image):
        assert ApartmentImage.objects.count() == 1
        delete_apartment_image_obj(
            image_id=db_image.id, apartment_id=db_image.apartment_id
        )
        assert ApartmentImage.objects.count() == 0

    def test_get_main_image_return_apartment_image_with_is_main_true(
        self, db_image, db_image_main
    ):
        main_image_queryset = _get_main_image(apartment_id=db_image.apartment_id)
        assert main_image_queryset.exists()
        main_image = main_image_queryset.first()
        assert main_image.is_main is True
        assert main_image == db_image_main

    def test_update_apartment_image_obj_set_(
        self, db_image_main, db_image
    ):
        update_apartment_image_obj(
            image_obj=db_image, apartment_id=db_image.apartment_id
        )
        assert db_image.is_main is True
        db_image_main.refresh_from_db()
        assert db_image_main.is_main is False
