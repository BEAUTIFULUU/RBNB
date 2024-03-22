from typing import Type

from django.db.models import QuerySet
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.views import APIView
from visits.serializers import VisitInputSerializer, VisitOutputSerializer
from visits.services import create_apartment_visit, get_owner_apartments_visits


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


class VisitView(generics.ListAPIView):
    serializer_class = VisitOutputSerializer

    def get_queryset(self) -> QuerySet:
        return get_owner_apartments_visits(owner_id=self.request.user.id)
