from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    """
    Serializer for data from ImageView
    """
    name = serializers.CharField()
    file = serializers.CharField()
