from unittest.mock import patch

from PIL import Image
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.prediction.PredictionView import PredictionView
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions


class TestPredictionView(APITestCase):
    """
    Test PredictionView
    """

    def setUp(self):
        self.url = reverse('prediction', kwargs={'dataset': 'dataset', 'prediction': 'pred', 'image_name': 'image.jpg'})
        self.user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=self.user)
        self.settings = {"stroke_size": 15, "show_colored": "true", "show_labeled": "true", "font_size": 35,
                         "classes": ["class", "class2"], "colors": ["color1", "color2"], "min_conf": 10, "max_conf": 90,
                         "nms_iou": 0.5, "nms_score": 0.5, "only_ground_truth": False, "ground_truth_iou": 0}
        self.view = PredictionView()

    def test_prediction_view_without_dataset(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Dataset does not exist yet")

    def test_ground_truth_view_without_ground_truth(self):
        Dataset.objects.create(name="dataset", userId=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Prediction file does not exist yet")

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_files_from_dir')
    def test_ground_truth_view_without_correct_image(self, get_files_from_dir):
        get_files_from_dir.return_value = ["test_image1.jpg", "test_image2.png"]

        dataset = Dataset.objects.create(name="dataset", userId=self.user)
        Predictions.objects.create(name="pred", datasetId=dataset, userId=self.user)

        response = self.client.get(self.url, data=self.settings)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Image not found in dataset")

    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.draw_bounding_boxes')
    @patch('ObjectDetectionAnalyzer.prediction.PredictionView.PredictionView.filter_predictions')
    @patch('ObjectDetectionAnalyzer.services.CSVParseService.CSVParseService.get_values_for_image')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_files_from_dir')
    def test_ground_truth_view_with_correct_image(self, get_files_from_dir, get_values_for_image, filter_predictions,
                                                  draw_bounding_boxes):
        get_files_from_dir.return_value = ["image.jpg", "image2.png"]
        values = [{'class': 'class1', 'confidence': 50, 'xmin': 0, 'ymin': 0, 'xmax': 10, 'ymax': 10}]
        get_values_for_image.return_value = values
        filter_predictions.return_value = values
        draw_bounding_boxes.return_value = Image.new('RGBA', (100, 100), (255, 0, 0, 0))

        dataset = Dataset.objects.create(name="dataset", userId=self.user)
        Predictions.objects.create(name="pred", datasetId=dataset, userId=self.user)

        response = self.client.get(self.url, data=self.settings)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'image.jpg')

    @patch('ObjectDetectionAnalyzer.services.FilterPredictionsService.FilterPredictionsService.get_nms_predictions')
    @patch(
        'ObjectDetectionAnalyzer.services.FilterPredictionsService.FilterPredictionsService.get_interval_predictions')
    def test_filter_predictions(self, get_interval_predictions, get_nms_predictions):
        values = [{'class': 'class1', 'confidence': 50, 'xmin': 0, 'ymin': 0, 'xmax': 10, 'ymax': 10}]

        self.view.filter_predictions(values, self.settings)

        get_interval_predictions.assert_called()
        get_nms_predictions.assert_called()

    @patch('ObjectDetectionAnalyzer.prediction.PredictionView.PredictionView.draw_ground_truth_matches')
    def test_draw_predictions_only_ground_truth(self, draw_ground_truth_matches):
        settings = {"stroke_size": 15, "show_colored": "true", "show_labeled": "true", "font_size": 35,
                    "classes": ["class", "class2"], "colors": ["color1", "color2"], "min_conf": 10,
                    "max_conf": 90,
                    "nms_iou": 0.5, "nms_score": 0.5, "only_ground_truth": True, "ground_truth_iou": 0.5}
        draw_ground_truth_matches.return_value = "some_image"
        values = [{'class': 'class1', 'confidence': 50, 'xmin': 0, 'ymin': 0, 'xmax': 10, 'ymax': 10}]
        dataset = Dataset.objects.create(name="dataset", userId=self.user)

        result = self.view.draw_predictions(dataset, "image.jpg", "some_image", values, settings)

        self.assertEqual(result, "some_image")

    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.draw_bounding_boxes')
    @patch('ObjectDetectionAnalyzer.prediction.PredictionView.PredictionView.draw_ground_truth_matches')
    def test_draw_predictions_ground_truth_iou(self, draw_ground_truth_matches, draw_bounding_boxes):
        settings = {"stroke_size": 15, "show_colored": "true", "show_labeled": "true", "font_size": 35,
                    "classes": ["class", "class2"], "colors": ["color1", "color2"], "min_conf": 10,
                    "max_conf": 90,
                    "nms_iou": 0.5, "nms_score": 0.5, "only_ground_truth": False, "ground_truth_iou": 0.5}

        draw_ground_truth_matches.return_value = "some_image"
        draw_bounding_boxes.return_value = "pred_image"
        dataset = Dataset.objects.create(name="dataset", userId=self.user)
        values = [{'class': 'class1', 'confidence': 50, 'xmin': 0, 'ymin': 0, 'xmax': 10, 'ymax': 10}]

        result = self.view.draw_predictions(dataset, "image.jpg", "some_image", values, settings)

        self.assertEqual(result, "pred_image")

    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.draw_bounding_boxes')
    def test_draw_predictions_without_ground_truth(self, draw_bounding_boxes):
        settings = {"stroke_size": 15, "show_colored": "true", "show_labeled": "true", "font_size": 35,
                    "classes": ["class", "class2"], "colors": ["color1", "color2"], "min_conf": 10,
                    "max_conf": 90,
                    "nms_iou": 0.5, "nms_score": 0.5, "only_ground_truth": False, "ground_truth_iou": 0}

        draw_bounding_boxes.return_value = "pred_image"
        dataset = Dataset.objects.create(name="dataset", userId=self.user)
        values = [{'class': 'class1', 'confidence': 50, 'xmin': 0, 'ymin': 0, 'xmax': 10, 'ymax': 10}]

        result = self.view.draw_predictions(dataset, "image.jpg", "some_image", values, settings)

        self.assertEqual(result, "pred_image")

    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.draw_gt_boxes')
    @patch(
        'ObjectDetectionAnalyzer.services.FilterPredictionsService.FilterPredictionsService.get_ground_truth_results')
    @patch('ObjectDetectionAnalyzer.services.CSVParseService.CSVParseService.get_values_for_image')
    def test_draw_ground_truth_matches(self, get_values_for_image, get_ground_truth_results, draw_gt_boxes):
        values = [{'class': 'class1', 'confidence': 50, 'xmin': 0, 'ymin': 0, 'xmax': 10, 'ymax': 10}]
        get_values_for_image.return_value = values
        get_ground_truth_results.return_value = values
        draw_gt_boxes.return_value = "pred_image"

        dataset = Dataset.objects.create(name="dataset", userId=self.user)

        result = self.view.draw_ground_truth_matches(dataset, "image.jpg", "image_path", "some_image", self.settings)

        self.assertEqual(result, "pred_image")
