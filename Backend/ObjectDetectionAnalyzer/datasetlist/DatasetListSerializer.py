from rest_framework import serializers


class DatasetListSerializer(serializers.Serializer):
    name = serializers.CharField()
    ground_truth = serializers.BooleanField()
    classes = serializers.ListField(str)
    colors = serializers.ListField(str)
    predictions = serializers.BooleanField()
