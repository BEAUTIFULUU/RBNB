from typing import Type

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Apartment
from .serializers import (
    ApartmentOutputSerializer,
    ApartmentInputSerializer,
    ApartmentDetailOutputSerializer,
)
from .services import (
    list_apartments,
    get_apartment_details,
    list_user_apartment_advertisements,
    create_apartment_with_address,
    update_apartment_with_address,
)


class ApartmentView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["price", "deposit", "is_available"]
    serializer_class = ApartmentOutputSerializer

    def get_queryset(self) -> list[Apartment]:
        return list_apartments()


class ApartmentDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApartmentDetailOutputSerializer
    lookup_field = "apartment_id"

    def get_object(self) -> Apartment:
        apartment_id = self.kwargs["apartment_id"]
        return get_apartment_details(apartment_id)


class ApartmentAdvertiseView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(
        self,
    ) -> Type[ApartmentDetailOutputSerializer | ApartmentInputSerializer]:
        return (
            ApartmentDetailOutputSerializer
            if self.request.method == "GET"
            else ApartmentInputSerializer
        )

    def get_queryset(self) -> list[Apartment]:
        return list_user_apartment_advertisements(self.request.user.id)

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        apartment_obj = create_apartment_with_address(
            data=serializer.validated_data, owner_id=self.request.user.id
        )
        output_serializer = ApartmentDetailOutputSerializer(apartment_obj)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ApartmentAdvertiseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "apartment_id"

    def get_serializer_class(
        self,
    ) -> Type[ApartmentDetailOutputSerializer | ApartmentInputSerializer]:
        return (
            ApartmentDetailOutputSerializer
            if self.request.method == "GET"
            else ApartmentInputSerializer
        )

    def get_object(self) -> Apartment:
        apartment_id = self.kwargs["apartment_id"]
        return get_apartment_details(apartment_id=apartment_id)

    def update(self, request, *args, **kwargs) -> Response:
        apartment_obj = self.get_object()
        serializer = self.get_serializer(
            instance=apartment_obj, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        update_apartment_with_address(
            data=serializer.validated_data, apartment_obj=apartment_obj
        )
        output_serializer = ApartmentDetailOutputSerializer(apartment_obj)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
