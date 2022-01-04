from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.upload.UploadModels import Dataset


class TestDatasetListView(APITestCase):
    """
    Test ImageFilesView
    """

    def setUp(self):
        self.url = reverse('dataset-list')
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
