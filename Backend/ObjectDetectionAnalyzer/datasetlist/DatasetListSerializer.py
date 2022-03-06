from rest_framework import serializers


class DatasetListSerializer(serializers.Serializer):
    """
    Serializer for data from DatasetListView
    """
    name = serializers.CharField()
    ground_truth = serializers.BooleanField()
    classes = serializers.ListField(child=serializers.CharField(max_length=50))
    colors = serializers.ListField(child=serializers.CharField(max_length=20))
    predictions = serializers.BooleanField()
