from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.datasetlist.DatasetListSerializer import DatasetListSerializer
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset


class DatasetListView(APIView):
    """
    Handle requests sent to /dataset-list
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Send image with name image_name from data directory.
        """
        user = request.user

        response_data = [
            {'name': dataset.name} for dataset in Dataset.objects.filter(userId=user)
        ]

        serializer = DatasetListSerializer(response_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
