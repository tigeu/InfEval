from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.predictionlist.PredictionListSerializer import PredictionListSerializer
from ObjectDetectionAnalyzer.services.PathService import PathService
from ObjectDetectionAnalyzer.settings import DATA_DIR
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions


class PredictionListView(APIView):
    """
    Handle requests sent to /prediction-list
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path_service = PathService()

    def get(self, request, dataset):
        user = request.user

        filtered_dataset = Dataset.objects.filter(name=dataset, userId=user)
        if not filtered_dataset:
            return Response("Dataset does not exist yet", status=status.HTTP_404_NOT_FOUND)

        predictions = Predictions.objects.filter(datasetId=filtered_dataset.first(), userId=user)
        if not predictions:
            return Response("No predictions available for this dataset yet", status=status.HTTP_404_NOT_FOUND)

        user_dir = self.path_service.get_combined_dir(DATA_DIR, request.user.username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset)

        response_data = [
            {'name': prediction.name} for prediction in predictions
        ]

        serializer = PredictionListSerializer(response_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
