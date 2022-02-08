from rest_framework import serializers


class ModelListSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
