import base64
import io
from pathlib import Path

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.prediction.PredictionSerializer import PredictionSerializer
from ObjectDetectionAnalyzer.services.CSVParseService import CSVParseService
from ObjectDetectionAnalyzer.services.DrawBoundingBoxService import DrawBoundingBoxService
from ObjectDetectionAnalyzer.services.PathService import PathService
from ObjectDetectionAnalyzer.settings import PREDICTION_INDICES
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions


class PredictionView(APIView):
    parser_classes = [MultiPartParser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path_service = PathService()
        self.csv_parse_service = CSVParseService()
        self.draw_bounding_box_service = DrawBoundingBoxService()

    def get(self, request, dataset, prediction, image_name):
        user = request.user

        filtered_dataset = Dataset.objects.filter(name=dataset, userId=user)
        if not filtered_dataset:
            return Response("Dataset does not exist yet", status=status.HTTP_404_NOT_FOUND)

        dataset = filtered_dataset.first()
        filtered_pred = Predictions.objects.filter(name=prediction, datasetId=filtered_dataset.first(), userId=user)
        if not filtered_pred:
            return Response("Prediction file does not exist yet", status=status.HTTP_404_NOT_FOUND)

        pred = filtered_pred.first()

        settings = {
            'stroke_size': int(request.GET['stroke_size']),
            'show_colored': request.GET['show_colored'].lower() == "true",
            'show_labeled': request.GET['show_labeled'].lower() == "true",
            'font_size': int(request.GET['font_size']),
        }

        indices = PREDICTION_INDICES
        dataset_files = self.path_service.get_files_from_dir(dataset.path)
        if image_name in dataset_files:
            predictions = self.csv_parse_service.get_values_for_image(pred.path, image_name, indices)
            classes = self.csv_parse_service.get_classes(dataset.ground_truth_path, indices['class'])
            image_path = Path(dataset.path) / image_name
            pred_image = self.draw_bounding_box_service.draw_bounding_boxes(predictions, image_path, classes, settings)

            with io.BytesIO() as output:
                pred_image.save(output, format="PNG")
                image_base64 = base64.b64encode(output.getvalue()).decode('utf-8')

            response_data = {
                'name': image_name,
                'file': image_base64
            }

            serializer = PredictionSerializer(response_data)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("Image not found in dataset", status=status.HTTP_404_NOT_FOUND)
