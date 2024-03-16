from PIL import Image as PILImage
import uuid
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from images.models import ApartmentImage
from images.validators import validate_image_format


def create_apartment_image_obj(
    image: InMemoryUploadedFile, advertisement_id: int
) -> ApartmentImage:
    validate_image_format(uploaded_image=image)
    image.name = f"{uuid.uuid4()}_adv_id: {advertisement_id}.jpg"
    return ApartmentImage.objects.create(image=image, apartment_id=advertisement_id)


def get_apartment_image_details(
    apartment_id: int, image_id: uuid.UUID
) -> ApartmentImage:
    image_obj = ApartmentImage.objects.filter(
        id=image_id, apartment_id=apartment_id
    ).select_related("apartment")
    return get_object_or_404(image_obj)


def delete_apartment_image_obj(image_id: uuid.UUID, apartment_id: int) -> None:
    image_obj = get_object_or_404(
        ApartmentImage, id=image_id, apartment_id=apartment_id
    )
    image_obj.delete()


def _get_main_image(apartment_id: int) -> QuerySet:
    return ApartmentImage.objects.filter(apartment_id=apartment_id, is_main=True)


def update_apartment_image_obj(image_obj: ApartmentImage, apartment_id: int) -> None:
    ApartmentImage.objects.filter(apartment_id=apartment_id).update(is_main=False)
    image_obj.is_main = True
    image_obj.save()


def get_image_resolution(image: ApartmentImage) -> str:
    with image.image.open("rb") as image_file:
        img = PILImage.open(image_file)
        return f"width: {img.width} height: {img.height}"
