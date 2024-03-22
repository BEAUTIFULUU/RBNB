from typing import Type
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.views import APIView
from visits.serializers import VisitInputSerializer
from visits.services import create_apartment_visit


class VisitView(APIView):
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
