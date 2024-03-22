from rest_framework import serializers
from visits.models import Visit


class VisitInputSerializer(serializers.Serializer):
    date_time = serializers.DateTimeField()


class VisitDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ["id", "apartment", "date_time", "state"]
        read_only = True
