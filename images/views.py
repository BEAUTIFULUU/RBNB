from typing import Type

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status, generics
from images.services import create_image_obj, get_image_details, update_image_obj
from images.models import ApartmentImage
from images.serializers import ImageDetailOutputSerializer, ImageDetailInputSerializer
from images.permissions import IsOwnerOrForbidden


class AdvertisementImageView(generics.CreateAPIView):
    permission_classes = [IsOwnerOrForbidden]
    parser_classes = [MultiPartParser]
    lookup_field = "advertisement_id"

    def create(self, request: Request, *args, **kwargs) -> Response:
        images = request.FILES.getlist("images")
        for image in images:
            create_image_obj(
                image=image, advertisement_id=self.kwargs["advertisement_id"]
            )
        return Response(status=status.HTTP_201_CREATED)


class AdvertisementImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrForbidden]

    def get_serializer_class(
        self,
    ) -> Type[ImageDetailOutputSerializer | ImageDetailInputSerializer]:
        return (
            ImageDetailOutputSerializer
            if self.request.method == "GET"
            else ImageDetailInputSerializer
        )

    def get_object(self) -> ApartmentImage:
        return get_image_details(
            apartment_id=self.kwargs["advertisement_id"],
            image_id=self.kwargs["image_id"],
        )

    def update(self, request: Request, *args, **kwargs) -> Response:
        image_obj = self.get_object()
        serializer = self.get_serializer(instance=image_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        update_image_obj(
            image_obj=image_obj, apartment_id=self.kwargs["advertisement_id"]
        )
        output_serializer = ImageDetailOutputSerializer(image_obj)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
