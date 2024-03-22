from rest_framework import serializers
from visits.models import Visit
from visits.validators import validate_apartment_visit_date


class VisitInputSerializer(serializers.Serializer):
    date_time = serializers.DateTimeField(validators=[validate_apartment_visit_date])


class VisitOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ["id", "apartment", "date_time", "state"]
        read_only = True
