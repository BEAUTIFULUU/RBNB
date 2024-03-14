from typing import Type

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.request import Request
from apartments.models import Apartment
from apartments.serializers import (
    ApartmentOutputSerializer,
    ApartmentInputSerializer,
    ApartmentDetailOutputSerializer,
)
from apartments.services import (
    list_apartments,
    get_apartment_details,
    list_owner_apartments,
    create_apartment,
    update_apartment,
    get_apartment_advertisement_details,
)


class ApartmentView(generics.ListAPIView):
    serializer_class = ApartmentOutputSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "price": ["gte", "lte"],
        "surface": ["gte", "lte"],
        "is_available": ["exact"],
    }

    def get_queryset(self) -> QuerySet[Apartment]:
        return list_apartments()


class ApartmentDetailView(generics.RetrieveAPIView):
    serializer_class = ApartmentDetailOutputSerializer
    lookup_field = "apartment_id"

    def get_object(self) -> Apartment:
        apartment_id = self.kwargs["apartment_id"]
        return get_apartment_details(apartment_id)


class ApartmentAdvertisementView(generics.ListCreateAPIView):
    def get_serializer_class(
        self,
    ) -> Type[ApartmentOutputSerializer | ApartmentInputSerializer]:
        return (
            ApartmentOutputSerializer
            if self.request.method == "GET"
            else ApartmentInputSerializer
        )

    def get_queryset(self) -> QuerySet[Apartment]:
        return list_owner_apartments(owner_id=self.request.user.id)

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        apartment_obj = create_apartment(
            data=serializer.validated_data, owner=self.request.user.id
        )
        output_serializer = ApartmentDetailOutputSerializer(apartment_obj)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ApartmentAdvertisementDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "advertisement_id"

    def get_serializer_class(
        self,
    ) -> Type[ApartmentDetailOutputSerializer | ApartmentInputSerializer]:
        return (
            ApartmentDetailOutputSerializer
            if self.request.method == "GET"
            else ApartmentInputSerializer
        )

    def get_object(self) -> Apartment:
        apartment_id = self.kwargs["advertisement_id"]
        owner_id = self.request.user.id
        return get_apartment_advertisement_details(
            apartment_id=apartment_id, owner_id=owner_id
        )

    def update(self, request: Request, *args, **kwargs) -> Response:
        apartment_obj = self.get_object()
        serializer = self.get_serializer(
            instance=apartment_obj, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        update_apartment(data=serializer.validated_data, apartment_obj=apartment_obj)
        output_serializer = ApartmentDetailOutputSerializer(apartment_obj)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
