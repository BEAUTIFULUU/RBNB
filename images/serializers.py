from rest_framework import serializers
from images.models import ApartmentImage
from images.services import get_image_resolution


class ImageOutputSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = ApartmentImage
        fields = ["id", "image", "is_main"]
        many = True

    def get_image(self, instance):
        if instance.image:
            return instance.image.url
        return None


class ImageOutputSimpleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ApartmentImage
        fields = ["id", "image"]
        many = True

    def get_image(self, instance):
        if instance.image:
            return instance.image.url
        return None


class ImageDetailOutputSerializer(serializers.ModelSerializer):
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


class ImageDetailInputSerializer(serializers.Serializer):
    is_main = serializers.BooleanField(default=False)
