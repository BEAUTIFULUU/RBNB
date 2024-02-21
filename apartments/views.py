from typing import Type

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, permissions, views
from .models import Apartment, Address
from .permissions import IsAdminOrReadOnly
from .serializers import (
    ApartmentOutputSerializer,
    ApartmentInputSerializer,
    ApartmentDetailOutputSerializer,
    UserOutputSerializer,
)
from .services import (
    list_apartments,
    get_apartment_details,
)


class UserDetailsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserOutputSerializer

    def get_object(self):
        return self.request.user


class ApartmentView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["price", "deposit", "is_available"]
    serializer_class = ApartmentOutputSerializer

    def get_queryset(self) -> list[Apartment]:
        return list_apartments()


class ApartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "apartment_id"

    def get_serializer_class(
        self,
    ) -> Type[ApartmentOutputSerializer | ApartmentInputSerializer]:
        return (
            ApartmentDetailOutputSerializer
            if self.request.method == "GET"
            else ApartmentInputSerializer
        )

    def get_object(self) -> Apartment:
        apartment_id = self.kwargs["apartment_id"]
        return get_apartment_details(apartment_id)

    def update(self, request, *args, **kwargs) -> Response:
        apartment_obj = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        output_serializer = ApartmentDetailOutputSerializer(apartment_obj)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
