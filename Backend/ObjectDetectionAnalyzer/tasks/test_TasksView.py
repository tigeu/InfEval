from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.upload.UploadModels import Models


class TestTasksView(APITestCase):
    """
    Test TasksView
    """

    def setUp(self):
        self.url = reverse('tasks')
        self.model1 = Models(name="model1", type="tf2")
        self.model2 = Models(name="model2", type="pytorch")
        self.model3 = Models(name="model3", type="yolov3")
        self.model_list = [self.model1, self.model2, self.model3]

    @patch('ObjectDetectionAnalyzer.upload.UploadModels.Models.objects.filter')
    def test_dataset_list_with_datasets(self, filter):
        """
        Test that correct image is returned
        """
        filter.return_value = self.model_list
        user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], {"name": "model1", "type": "tf2"})
        self.assertEqual(response.data[1], {"name": "model2", "type": "pytorch"})
        self.assertEqual(response.data[2], {"name": "model3", "type": "yolov3"})

    @patch('ObjectDetectionAnalyzer.upload.UploadModels.Models.objects.filter')
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
