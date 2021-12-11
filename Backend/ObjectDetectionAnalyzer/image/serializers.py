from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    name = serializers.CharField()
    file = serializers.CharField()
