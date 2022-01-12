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

        response_data = []
        for dataset in Dataset.objects.filter(userId=user):
            data = {'name': dataset.name}
            if dataset.ground_truth_path:
                data['ground_truth'] = True
            if dataset.label_map_path:
                data['label_map'] = True

            response_data.append(data)

        serializer = DatasetListSerializer(response_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
