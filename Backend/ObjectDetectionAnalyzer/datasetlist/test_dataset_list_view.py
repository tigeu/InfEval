from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions


class TestDatasetListView(APITestCase):
    """
    Test ImageFilesView
    """

    def setUp(self):
        self.url = reverse('dataset-list')
        self.delete_url = reverse('dataset-list', kwargs={'dataset': 'dataset'})
        self.dataset1 = Dataset(name="dataset1")
        self.dataset2 = Dataset(name="dataset2")
        self.dataset3 = Dataset(name="dataset3")
        self.dataset_list = [self.dataset1, self.dataset2, self.dataset3]

    @patch('ObjectDetectionAnalyzer.upload.UploadModels.Dataset.objects.filter')
    def test_dataset_list_with_datasets(self, filter):
        """
        Test that correct image is returned
        """
        filter.return_value = self.dataset_list
        user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], "dataset1")
        self.assertEqual(response.data[1]['name'], "dataset2")
        self.assertEqual(response.data[2]['name'], "dataset3")

    @patch('ObjectDetectionAnalyzer.services.ColorService.ColorService.get_class_colors')
    @patch('ObjectDetectionAnalyzer.services.CSVParseService.CSVParseService.get_classes')
    def test_dataset_list_with_ground_truth(self, get_classes, get_class_colors):
        user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=user)

        Dataset.objects.create(name="dataset_name", ground_truth_path="path", userId=user)
        get_classes.return_value = ["class1", "class2"]
        get_class_colors.return_value = ["color1", "color2"]

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], "dataset_name")
        self.assertEqual(response.data[0]['ground_truth'], True)
        self.assertEqual(response.data[0]['classes'], ["class1", "class2"])
        self.assertEqual(response.data[0]['colors'], ["color1", "color2"])
        self.assertEqual(response.data[0]['predictions'], False)

    def test_dataset_list_without_ground_truth(self):
        user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=user)

        Dataset.objects.create(name="dataset_name", userId=user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], "dataset_name")
        self.assertEqual(response.data[0]['ground_truth'], False)
        self.assertEqual(response.data[0]['predictions'], False)

    def test_dataset_list_without_ground_truth_with_predictions(self):
        user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=user)

        dataset = Dataset.objects.create(name="dataset_name", userId=user)
        Predictions.objects.create(name="pred", datasetId=dataset, userId=user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], "dataset_name")
        self.assertEqual(response.data[0]['ground_truth'], False)
        self.assertEqual(response.data[0]['predictions'], True)

    @patch('ObjectDetectionAnalyzer.upload.UploadModels.Dataset.objects.filter')
    def test_dataset_list_with_without_data(self, filter):
        """
        Test that 404 not found is returned
        """
        filter.return_value = []

        user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_dataset_list_with_no_authentication(self):
        """
        Test that user without authentication gets 401
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('ObjectDetectionAnalyzer.upload.UploadModels.Dataset.delete')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.delete')
    def test_delete(self, path_delete, delete):
        user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=user)

        Dataset.objects.create(name="dataset", userId=user)

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Successfully deleted dataset")
        path_delete.assert_called()
        delete.assert_called()
