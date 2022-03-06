from rest_framework import serializers


class GroundTruthSerializer(serializers.Serializer):
    """
    Serializer for data from GroundTruthView
    """
    name = serializers.CharField()
    file = serializers.CharField()
