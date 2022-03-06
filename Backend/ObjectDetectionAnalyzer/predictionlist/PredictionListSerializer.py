from rest_framework import serializers


class PredictionListSerializer(serializers.Serializer):
    """
    Serializer for data from PredictionListView
    """
    name = serializers.CharField()
    classes = serializers.ListField()
    colors = serializers.ListField()
