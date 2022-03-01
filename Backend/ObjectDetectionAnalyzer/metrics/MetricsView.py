from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.metrics.MetricsService import MetricsService
from ObjectDetectionAnalyzer.services.CSVParseService import CSVParseService
from ObjectDetectionAnalyzer.services.FilterPredictionsService import FilterPredictionsService
from ObjectDetectionAnalyzer.settings import PREDICTION_INDICES, GROUND_TRUTH_INDICES
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions


class MetricsView(APIView):
    parser_classes = [MultiPartParser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.csv_parse_service = CSVParseService()
        self.filter_predictions_service = FilterPredictionsService()
        self.metrics_service = MetricsService()

    def get(self, request, dataset, prediction):
        user = request.user

        filtered_dataset = Dataset.objects.filter(name=dataset, userId=user)
        if not filtered_dataset:
            return Response("Dataset does not exist yet", status=status.HTTP_404_NOT_FOUND)

        dataset = filtered_dataset.first()
        filtered_pred = Predictions.objects.filter(name=prediction, datasetId=filtered_dataset.first(), userId=user)
        if not filtered_pred:
            return Response("Prediction file does not exist yet", status=status.HTTP_404_NOT_FOUND)

        pred = filtered_pred.first()

        settings = self.extract_prediction_settings(request.GET)
        image_name = settings['image_name']
        gt_path = dataset.ground_truth_path

        if image_name:
            predictions = self.csv_parse_service.get_values_for_image(pred.path, image_name, PREDICTION_INDICES)
            gts = self.csv_parse_service.get_values_for_image(gt_path, image_name, GROUND_TRUTH_INDICES)
        else:
            predictions = self.csv_parse_service.get_values(pred.path, PREDICTION_INDICES)
            gts = self.csv_parse_service.get_values(gt_path, GROUND_TRUTH_INDICES)
        predictions = self.filter_predictions(predictions, settings)
        gts = self.filter_ground_truths(gts, settings)
        if settings['metric'] == 'coco':
            results = self.metrics_service.calculate_coco(gts, predictions, settings['classes'])
        else:
            results = self.metrics_service.calculate_pascal_voc(gts, predictions, settings['iou'], settings['classes'])

        return Response(results, status=status.HTTP_200_OK)

    def extract_prediction_settings(self, request):
        settings = {
            'metric': request['metric'],
            'iou': float(request['iou']),
            'image_name': request['image_name'],
            'classes': request['classes'].split(','),
            'nms_iou': float(request['nms_iou']),
            'nms_score': float(request['nms_score']),
            'min_conf': int(request['min_conf']),
            'max_conf': int(request['max_conf']),
        }
        return settings

    def filter_predictions(self, predictions, settings):
        min_conf, max_conf = settings['min_conf'], settings['max_conf']
        if max_conf > 0:
            predictions = self.filter_predictions_service.get_interval_predictions(predictions, min_conf, max_conf)
        nms_iou, nms_score = settings['nms_iou'], settings['nms_score']
        if nms_iou > 0 or nms_score > 0:
            predictions = self.filter_predictions_service.get_nms_predictions(predictions, nms_iou, nms_score)
        return predictions

    def filter_ground_truths(self, gts, settings):
        filtered_gts = []
        for gt in gts:
            if gt['class'] in settings['classes']:
                filtered_gts.append(gt)
        return filtered_gts
