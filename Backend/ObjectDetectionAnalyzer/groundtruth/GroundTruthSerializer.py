from rest_framework import serializers


class GroundTruthSerializer(serializers.Serializer):
    name = serializers.CharField()
    file = serializers.CharField()
