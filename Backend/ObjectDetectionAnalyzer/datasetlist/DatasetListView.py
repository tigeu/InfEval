from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.datasetlist.DatasetListSerializer import DatasetListSerializer
from ObjectDetectionAnalyzer.services.CSVParseService import CSVParseService
from ObjectDetectionAnalyzer.services.ColorService import ColorService
from ObjectDetectionAnalyzer.settings import GROUND_TRUTH_INDICES
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions


class DatasetListView(APIView):
    """
    Handle requests sent to /dataset-list
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.csv_parse_service = CSVParseService()
        self.color_service = ColorService()

    def get(self, request):
        """
        Send image with name image_name from data directory.
        """
        user = request.user

        datasets = Dataset.objects.filter(userId=user)

        response_data = []
        for dataset in datasets:
            data = {'name': dataset.name}
            if dataset.ground_truth_path:
                data['ground_truth'] = True
                classes = self.csv_parse_service.get_classes(dataset.ground_truth_path, GROUND_TRUTH_INDICES['class'])
                data['classes'] = classes
                data['colors'] = self.color_service.get_class_colors(classes)
            else:
                data['ground_truth'] = False
            predictions = Predictions.objects.filter(datasetId=dataset, userId=user)
            if predictions:
                data['predictions'] = True
            else:
                data['predictions'] = False
            response_data.append(data)

        serializer = DatasetListSerializer(response_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
