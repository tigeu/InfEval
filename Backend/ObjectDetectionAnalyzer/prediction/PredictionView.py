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
from ObjectDetectionAnalyzer.services.FilterPredictionsService import FilterPredictionsService
from ObjectDetectionAnalyzer.services.PathService import PathService
from ObjectDetectionAnalyzer.settings import PREDICTION_INDICES, GROUND_TRUTH_INDICES
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions


class PredictionView(APIView):
    """
    View that handles requests sent to /predictions.
    GET: Returns transparent image with drawn (filtered) predictions on it

    Attributes
    ----------
    path_service : PathService
        Service for handling file system tasks
    csv_path_service : CSVParseService
        Service for parsing CSV-files
    filter_predictions_service : FilterPredictionsService
        Service for filtering predictions based on settings
    draw_bounding_box_service : DrawBoundingBoxService
        Service for drawing bounding boxs based on settings

    Methods
    -------
    get(request, dataset, prediction, image_name)
        Returns transparent image with drawn (filtered) predictions on it
    extract_prediction_settings(request)
        Return a dictionary containing all settings for drawing and filtering
    filter_predictions(predictions, settings)
        Returns filtered predictions based on settings
    draw_predictions(dataset, image_name, image_path, predictions, settings)
        Return transparent image with drawn ground truths/predictions on it based on settings
    draw_ground_truth_matches(dataset, image_name, pred_image, predictions, settings)

    """
    parser_classes = [MultiPartParser]

    def __init__(self, **kwargs):
        """
        Initialise required services
        """
        super().__init__(**kwargs)
        self.path_service = PathService()
        self.csv_parse_service = CSVParseService()
        self.filter_predictions_service = FilterPredictionsService()
        self.draw_bounding_box_service = DrawBoundingBoxService()

    def get(self, request, dataset, prediction, image_name):
        """
        Returns transparent image with drawn (filtered) predictions on it

        Parameters
        ----------
        request : HttpRequest
            GET request
        dataset : str
            Name of current dataset
        prediction : str
            Name of current prediction file
        image_name : str
            Name of current image

        Returns
        -------
        Response
            Requested data with status code
        """
        user = request.user

        filtered_dataset = Dataset.objects.filter(name=dataset, userId=user)
        if not filtered_dataset:
            return Response("Dataset does not exist yet", status=status.HTTP_404_NOT_FOUND)

        dataset = filtered_dataset.first()
        filtered_pred = Predictions.objects.filter(name=prediction, datasetId=filtered_dataset.first(), userId=user)
        if not filtered_pred:
            return Response("Prediction file does not exist yet", status=status.HTTP_404_NOT_FOUND)

        pred = filtered_pred.first()

        settings = self.extract_prediction_settings(request)

        indices = PREDICTION_INDICES
        dataset_files = self.path_service.get_files_from_dir(dataset.path)
        if image_name in dataset_files:
            predictions = self.csv_parse_service.get_values_for_image(pred.path, image_name, indices)
            predictions = self.filter_predictions(predictions, settings)
            image_path = Path(dataset.path) / image_name
            pred_image = self.draw_predictions(dataset, image_name, image_path, predictions, settings)

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

    def extract_prediction_settings(self, request):
        """
        Return a dictionary containing all settings for drawing and filtering

        Parameters
        ----------
        request : HttpRequest
            GET request

        Returns
        -------
        dict
            Dictionary with all settings for drawing and filtering
        """
        settings = {
            'stroke_size': int(request.GET['stroke_size']),
            'show_colored': request.GET['show_colored'].lower() == "true",
            'show_labeled': request.GET['show_labeled'].lower() == "true",
            'font_size': int(request.GET['font_size']),
            'classes': request.GET['classes'].split(','),
            'colors': request.GET['colors'].split(','),
            'nms_iou': float(request.GET['nms_iou']),
            'nms_score': float(request.GET['nms_score']),
            'min_conf': int(request.GET['min_conf']),
            'max_conf': int(request.GET['max_conf']),
            'only_ground_truth': request.GET['only_ground_truth'].lower() == "true",
            'ground_truth_iou': float(request.GET['ground_truth_iou']),
            'ground_truth_transparent': request.GET['ground_truth_transparent'].lower() == "true",
        }
        return settings

    def filter_predictions(self, predictions, settings):
        """
        Returns filtered predictions based on settings

        Parameters
        ----------
        predictions : dict
            List of dictionaries, each representing a single prediction
        settings : dict
            Dictionary containing all settings for drawing and filtering

        Returns
        -------
        list
            List of dictionaries, each representing a single prediction
        """
        min_conf, max_conf = settings['min_conf'], settings['max_conf']
        if max_conf > 0:
            predictions = self.filter_predictions_service.get_interval_predictions(predictions, min_conf, max_conf)
        nms_iou, nms_score = settings['nms_iou'], settings['nms_score']
        if nms_iou > 0 or nms_score > 0:
            predictions = self.filter_predictions_service.get_nms_predictions(predictions, nms_iou, nms_score)
        return predictions

    def draw_predictions(self, dataset, image_name, image_path, predictions, settings):
        """
        Return transparent image with drawn predictions on it based on settings

        Parameters
        ----------
        dataset : Dataset
            Current dataset
        image_name : str
            Name of current image
        image_path : Path
            Path of current image
        predictions : list
            List of dictionaries, each representing a single prediction
        settings : dict
            Dictionary containing all settings for drawing and filtering

        Returns
        -------
        ImageDraw
            Image with all drawings on it
        """
        # only draw ground truth boxes without predictions
        if settings['only_ground_truth'] and settings['ground_truth_iou'] > 0:
            pred_image = self.draw_ground_truth_matches(dataset, image_name, image_path, predictions, settings)
        # draw predictions
        else:
            # first draw ground truth boxes, then predictions
            if settings['ground_truth_iou'] > 0:
                pred_image = self.draw_ground_truth_matches(dataset, image_name, image_path, predictions, settings)
                pred_image = self.draw_bounding_box_service.draw_bounding_boxes(predictions, pred_image, settings,
                                                                                False)
            # only draw predictions
            else:
                pred_image = self.draw_bounding_box_service.draw_bounding_boxes(predictions, image_path, settings)
        return pred_image

    def draw_ground_truth_matches(self, dataset, image_name, pred_image, predictions, settings):
        """
        Return transparent image with drawn ground truths on it based on settings

        Parameters
        ----------
        dataset : Dataset
            Current dataset
        image_name : str
            Name of current image
        pred_image : Path
            Path of current image
        predictions : list
            List of dictionaries, each representing a single prediction
        settings : dict
            Dictionary containing all settings for drawing and filtering

        Returns
        -------
        ImageDraw
            Image with all drawings on it
        """
        gt_indices = GROUND_TRUTH_INDICES
        gts = self.csv_parse_service.get_values_for_image(dataset.ground_truth_path, image_name, gt_indices)
        iou = settings['ground_truth_iou']
        boxes = self.filter_predictions_service.get_ground_truth_results(gts, predictions, iou)
        pred_image = self.draw_bounding_box_service.draw_gt_boxes(boxes, pred_image, settings)
        return pred_image
