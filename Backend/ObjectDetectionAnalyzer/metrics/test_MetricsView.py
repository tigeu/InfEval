from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.metrics.MetricsView import MetricsView
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions


class TestMetricsView(APITestCase):
    """
    Test MetricsView
    """

    def setUp(self):
        self.url = reverse('metrics', kwargs={'dataset': 'dataset', 'prediction': 'pred'})
        self.view = MetricsView()

        self.user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=self.user)

        self.request = {'metric': 'pascal', 'iou': '0.5', 'image_name': 'image.jpg', 'classes': 'class1,class2',
                        'nms_iou': '0.5', 'nms_score': '0.5', 'min_conf': '25', 'max_conf': '75'}
        self.settings = {'metric': 'pascal', 'iou': 0.5, 'image_name': 'image.jpg', 'classes': ['class1', 'class2'],
                         'nms_iou': 0.5, 'nms_score': 0.5, 'min_conf': 25, 'max_conf': 75}

    def test_metrics_view_no_dataset(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Dataset does not exist yet")

    def test_metrics_view_no_prediction(self):
        Dataset.objects.create(name="dataset", userId=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Prediction file does not exist yet")

    @patch('ObjectDetectionAnalyzer.metrics.MetricsService.MetricsService.calculate_pascal_voc')
    @patch('ObjectDetectionAnalyzer.metrics.MetricsView.MetricsView.filter_predictions')
    @patch('ObjectDetectionAnalyzer.services.CSVParseService.CSVParseService.get_values_for_image')
    def test_metrics_view_with_image(self, get_values_for_image, filter_predictions, calculate_pascal_voc):
        preds = ["pred1", "pred2", "pred3"]
        gts = ["gt1", "gt2", "gt3"]
        get_values_for_image.side_effect = [preds, gts]
        filter_predictions.return_value = ["pred1", "pred2"]
        calculate_pascal_voc.return_value = "results"

        dataset = Dataset.objects.create(name="dataset", userId=self.user)
        Predictions.objects.create(name="pred", userId=self.user, datasetId=dataset)

        response = self.client.get(self.url, data=self.request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "results")
        self.assertEqual(get_values_for_image.call_count, 2)
        filter_predictions.assert_called_with(preds, self.settings)
        calculate_pascal_voc.assert_called_with(gts, ["pred1", "pred2"], 0.5, ["class1", "class2"])

    @patch('ObjectDetectionAnalyzer.metrics.MetricsService.MetricsService.calculate_coco')
    @patch('ObjectDetectionAnalyzer.metrics.MetricsView.MetricsView.filter_predictions')
    @patch('ObjectDetectionAnalyzer.services.CSVParseService.CSVParseService.get_values')
    def test_metrics_view_without_image(self, get_values, filter_predictions, calculate_coco):
        preds = ["pred1", "pred2", "pred3"]
        gts = ["gt1", "gt2", "gt3"]
        get_values.side_effect = [preds, gts]
        filter_predictions.return_value = ["pred1", "pred2"]
        calculate_coco.return_value = "results"

        request = {'metric': 'coco', 'iou': '0.5', 'image_name': '', 'classes': 'class1,class2',
                   'nms_iou': '0.5', 'nms_score': '0.5', 'min_conf': '25', 'max_conf': '75'}
        settings = {'metric': 'coco', 'iou': 0.5, 'image_name': '', 'classes': ['class1', 'class2'],
                    'nms_iou': 0.5, 'nms_score': 0.5, 'min_conf': 25, 'max_conf': 75}

        dataset = Dataset.objects.create(name="dataset", userId=self.user)
        Predictions.objects.create(name="pred", userId=self.user, datasetId=dataset)

        response = self.client.get(self.url, data=request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "results")
        self.assertEqual(get_values.call_count, 2)
        filter_predictions.assert_called_with(preds, settings)
        calculate_coco.assert_called_with(gts, ["pred1", "pred2"], ["class1", "class2"])

    def test_extract_prediction_settings(self):
        results = self.view.extract_prediction_settings(self.request)

        self.assertEqual(results, self.settings)

    @patch("ObjectDetectionAnalyzer.services.FilterPredictionsService.FilterPredictionsService.get_nms_predictions")
    @patch(
        "ObjectDetectionAnalyzer.services.FilterPredictionsService.FilterPredictionsService.get_interval_predictions")
    def test_overview_view(self, get_interval_predictions, get_nms_predictions):
        predictions = ["pred1", "pred2", "pred3"]
        get_interval_predictions.return_value = ["pred1", "pred2"]
        get_nms_predictions.return_value = ["pred1"]

        results = self.view.filter_predictions(predictions, self.settings)

        self.assertEqual(results, ["pred1"])
        get_interval_predictions.assert_called_with(predictions, 25, 75)
        get_nms_predictions.assert_called_with(["pred1", "pred2"], 0.5, 0.5)
