from rest_framework import serializers


class PredictionListSerializer(serializers.Serializer):
    name = serializers.CharField()
