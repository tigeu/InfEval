from rest_framework import serializers


class PredictionSerializer(serializers.Serializer):
    """
    Serializer for data from PredictionView
    """
    name = serializers.CharField()
    file = serializers.CharField()
