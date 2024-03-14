from rest_framework import serializers
from images.models import ApartmentImage
from images.services import get_image_resolution


class ApartmentImageOutputSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = ApartmentImage
        fields = ["id", "image", "is_main"]
        many = True

    def get_image(self, instance):
        if instance.image:
            return instance.image.url
        return None


class ApartmentImageOutputSimpleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ApartmentImage
        fields = ["id", "image"]
        many = True

    def get_image(self, instance):
        if instance.image:
            return instance.image.url
        return None


class ApartmentImageDetailOutputSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    resolution = serializers.SerializerMethodField()

    class Meta:
        model = ApartmentImage
        fields = ["id", "image", "is_main", "resolution"]

    def get_image(self, instance):
        if instance.image:
            return instance.image.url
        return None

    def get_resolution(self, obj):
        return get_image_resolution(image=obj)


class ApartmentImageDetailInputSerializer(serializers.Serializer):
    is_main = serializers.BooleanField(default=False)


class ApartmentImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField())
