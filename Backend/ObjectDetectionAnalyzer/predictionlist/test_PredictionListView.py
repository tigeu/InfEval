from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions


class TestPredictionListView(APITestCase):
    """
    Test PredictionListView
    """

    def setUp(self):
        self.url = reverse('prediction-list', kwargs={'dataset': 'dataset'})

        self.user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=self.user)

    def test_prediction_list_without_dataset(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Dataset does not exist yet")

    def test_prediction_list_with_dataset_without_predictions(self):
        Dataset.objects.create(name="dataset", userId=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "No predictions available for this dataset yet")

    @patch('ObjectDetectionAnalyzer.services.ColorService.ColorService.get_class_colors')
    @patch('ObjectDetectionAnalyzer.services.CSVParseService.CSVParseService.get_classes')
    def test_prediction_list_with_dataset_with_predictions(self, get_classes, get_class_colors):
        get_classes.return_value = ["class1", "class2"]
        get_class_colors.return_value = ["color1", "color2"]

        dataset = Dataset.objects.create(name="dataset", userId=self.user)
        Predictions.objects.create(name="prediction1", datasetId=dataset, userId=self.user)
        Predictions.objects.create(name="prediction2", datasetId=dataset, userId=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], "prediction1")
        self.assertEqual(response.data[0]['classes'], ["class1", "class2"])
        self.assertEqual(response.data[0]['colors'], ["color1", "color2"])
        self.assertEqual(response.data[1]['name'], "prediction2")
        self.assertEqual(response.data[1]['classes'], ["class1", "class2"])
        self.assertEqual(response.data[1]['colors'], ["color1", "color2"])

    @patch('ObjectDetectionAnalyzer.upload.UploadModels.Predictions.delete')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.delete')
    def test_delete(self, path_delete, delete):
        dataset = Dataset.objects.create(name="dataset", userId=self.user)
        Predictions.objects.create(name="dataset", datasetId=dataset, userId=self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Successfully deleted prediction")
        path_delete.assert_called()
        delete.assert_called()
