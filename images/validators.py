import magic
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from livehere import settings


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
