import base64
import io
import os
from pathlib import Path

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.groundtruth.CSVParseService import CSVParseService
from ObjectDetectionAnalyzer.groundtruth.DrawBoundingBoxService import DrawBoundingBoxService
from ObjectDetectionAnalyzer.groundtruth.GroundTruthSerializer import GroundTruthSerializer
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset


class GroundTruthView(APIView):
    parser_classes = [MultiPartParser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.csv_parse_service = CSVParseService()
        self.draw_bounding_box_service = DrawBoundingBoxService()

    def get(self, request, dataset, image_name):
        user = request.user

        dataset = Dataset.objects.filter(name=dataset, userId=user).first()
        if not dataset:
            return Response("Dataset does not exist yet", status=status.HTTP_404_NOT_FOUND)

        if not dataset.ground_truth_path:
            return Response("Ground truth file for dataset does not exist yet", status=status.HTTP_404_NOT_FOUND)

        settings = {
            'stroke_size': int(request.GET['stroke_size']),
            'show_colored': request.GET['show_colored'].lower() == "true",
            'show_labeled': request.GET['show_labeled'].lower() == "true",
            'font_size': int(request.GET['font_size']),
        }

        dataset_files = os.listdir(dataset.path)
        if image_name in dataset_files:
            predictions = self.csv_parse_service.get_ground_truth_values(dataset.ground_truth_path, image_name)
            classes = self.csv_parse_service.get_ground_truth_classes(dataset.ground_truth_path)
            image_path = Path(dataset.path) / image_name
            gt_image = self.draw_bounding_box_service.draw_bounding_boxes(predictions, image_path, classes, settings)

            with io.BytesIO() as output:
                gt_image.save(output, format="PNG")
                image_base64 = base64.b64encode(output.getvalue()).decode('utf-8')

            response_data = {
                'name': image_name,
                'file': image_base64
            }

            serializer = GroundTruthSerializer(response_data)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)
