from rest_framework import serializers


class ImageFilesSerializer(serializers.Serializer):
    """
    Serializer for data from ImageFilesView
    """
    name = serializers.CharField()
