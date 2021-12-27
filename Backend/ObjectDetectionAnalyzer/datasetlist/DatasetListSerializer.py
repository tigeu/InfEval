from rest_framework import serializers


class DatasetListSerializer(serializers.Serializer):
    name = serializers.CharField()
