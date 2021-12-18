from rest_framework.serializers import Serializer, FileField


class UploadSerializer(Serializer):
    file_uploaded = FileField()
