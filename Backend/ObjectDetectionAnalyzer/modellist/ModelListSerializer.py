from rest_framework import serializers


class ModelListSerializer(serializers.Serializer):
    """
    Serializer for data from ModelListView
    """
    name = serializers.CharField()
    type = serializers.CharField()
