import mimetypes
import os

import pytest
from _pytest.fixtures import SubRequest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from images.services import validate_image_format


@pytest.fixture
def in_memory_image(request: SubRequest):
    filename = request.param
    test_image_path = os.path.join(os.path.dirname(__file__), "test_data", filename)
    content_type, _ = mimetypes.guess_type(test_image_path)
    with open(test_image_path, "rb") as f:
        file_content = f.read()
        in_memory_file = SimpleUploadedFile(filename, file_content, content_type)
    return in_memory_file


class TestImageValidation:
    @pytest.mark.parametrize("in_memory_image", ["valid_image.jpg"], indirect=True)
    def test_validate_image_format_return_none_if_image_valid(self, in_memory_image):
        try:
            validate_image_format(uploaded_image=in_memory_image)
        except ValidationError as e:
            pytest.fail(str(e))

    @pytest.mark.parametrize("in_memory_image", ["fake_jpg_file.jpg"], indirect=True)
    def test_validate_image_format_raises_validation_error_if_invalid_image_format(
        self, in_memory_image
    ):
        with pytest.raises(ValidationError) as e:
            validate_image_format(uploaded_image=in_memory_image)
            assert (
                str(e.value)
                == "Invalid image format. Only JPEG and PNG images are allowed."
            )

    @pytest.mark.parametrize(
        "in_memory_image", ["wrong_extension_image.ggg"], indirect=True
    )
    def test_validate_image_format_raises_validation_error_if_invalid_image_extension(
        self, in_memory_image
    ):
        with pytest.raises(ValidationError) as e:
            validate_image_format(uploaded_image=in_memory_image)
            assert str(e.value) == "Invalid image extension."
