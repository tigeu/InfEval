from rest_framework import serializers


class ImageFilesSerializer(serializers.Serializer):
    name = serializers.CharField()
