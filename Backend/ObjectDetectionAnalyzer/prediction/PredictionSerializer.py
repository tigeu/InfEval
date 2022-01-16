from rest_framework import serializers


class PredictionSerializer(serializers.Serializer):
    name = serializers.CharField()
    file = serializers.CharField()
