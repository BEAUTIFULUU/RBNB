from PIL import Image as PILImage
import magic
import uuid
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from images.models import ApartmentImage


def validate_image_format(uploaded_image: InMemoryUploadedFile) -> None:
    if uploaded_image is None:
        raise ValidationError("No image provided.")

    image_bytes = uploaded_image.read()
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(image_bytes[:2048])

    if not any(
        mime_type.startswith(content_type)
        for content_type in settings.WHITELISTED_IMAGE_TYPES.values()
    ):
        raise ValidationError(
            "Invalid image format. Only JPEG and PNG images are allowed."
        )

    extension = uploaded_image.name.split(".")[-1].lower()
    if extension not in settings.WHITELISTED_IMAGE_TYPES:
        raise ValidationError("Invalid image extension.")


def list_advertisement_images(apartment_id: int) -> QuerySet[ApartmentImage]:
    return ApartmentImage.objects.filter(apartment_id=apartment_id).select_related(
        "apartment"
    )


def create_image_obj(
    image: InMemoryUploadedFile, advertisement_id: int
) -> ApartmentImage:
    validate_image_format(uploaded_image=image)
    image.name = f"{uuid.uuid4()}_adv_id: {advertisement_id}.jpg"
    return ApartmentImage.objects.create(image=image, apartment_id=advertisement_id)


def get_image_details(apartment_id: int, image_id: uuid.UUID) -> ApartmentImage:
    image_obj = ApartmentImage.objects.filter(
        id=image_id, apartment_id=apartment_id
    ).select_related("apartment")
    return get_object_or_404(image_obj)


def delete_image_obj(image_id: uuid.UUID, apartment_id: int) -> None:
    image_obj = get_object_or_404(
        ApartmentImage, id=image_id, apartment_id=apartment_id
    )
    image_obj.delete()


def _get_main_image(apartment_id: int) -> QuerySet[ApartmentImage]:
    return ApartmentImage.objects.filter(
        apartment_id=apartment_id, is_main=True
    ).select_related("apartment")


def update_image_obj(image_obj: ApartmentImage, apartment_id: int) -> None:
    main_img = _get_main_image(apartment_id=apartment_id)
    if main_img.exists():
        main_img.update(is_main=False)

    image_obj.is_main = True
    image_obj.save()


def get_image_resolution(image: ApartmentImage) -> str:
    with image.image.open("rb") as image_file:
        img = PILImage.open(image_file)
        return f"width: {img.width} height: {img.height}"
