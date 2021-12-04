from rest_framework import serializers


class HeartbeatSerializer(serializers.Serializer):
    count = serializers.IntegerField()
