from typing import Type

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.views import APIView
from visits.serializers import VisitInputSerializer, VisitOutputSerializer
from visits.services import (
    create_apartment_visit,
    get_owner_apartments_visits,
    get_tenant_apartments_visits,
)


class CreateVisitView(APIView):
    serializer_class = VisitInputSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_apartment_visit(
            apartment_id=self.kwargs["apartment_id"],
            user_id=self.request.user.id,
            date_time=serializer.validated_data["date_time"],
        )
        return Response(status=status.HTTP_201_CREATED)


class OwnerVisitView(generics.ListAPIView):
    serializer_class = VisitOutputSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "date_time": ["gte", "lte"],
        "apartment": ["exact"],
        "state": ["exact"],
    }

    def get_queryset(self) -> QuerySet:
        return get_owner_apartments_visits(owner_id=self.request.user.id)


class TenantVisitView(generics.ListAPIView):
    serializer_class = VisitOutputSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "date_time": ["gte", "lte"],
        "apartment": ["exact"],
        "state": ["exact"],
    }

    def get_queryset(self):
        return get_tenant_apartments_visits(tenant_id=self.request.user.id)
