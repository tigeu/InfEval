from rest_framework import serializers


class TasksListSerializer(serializers.Serializer):
    """
    Serializer for data from TasksListView
    """
    name = serializers.CharField()
    description = serializers.CharField()
    fileName = serializers.CharField()
    progress = serializers.FloatField()
    started = serializers.DateTimeField()
    finished = serializers.DateTimeField()
    dataset = serializers.CharField()
    model = serializers.CharField()
