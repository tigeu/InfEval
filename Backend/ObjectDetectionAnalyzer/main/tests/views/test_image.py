from unittest.mock import MagicMock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.main.services.FileService import FileService


class test_image(APITestCase):
    """
    Test ImageView.py
    """

    def __init__(self, methodName='runTest'):
        super(test_image, self).__init__(methodName)

        self.url = reverse('image', kwargs={'image_name': "test_image.jpg"})

    def test_image_with_data(self):
        """
        Test that correct image is returned
        """
        FileService.encode_image = MagicMock(return_value=["dGVzdA=="])

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "test_image.jpg")
        self.assertEqual(response.data['file'], "['dGVzdA==']")

    def test_image_without_data(self):
        """
        Test that 404 not found is returned
        """
        FileService.encode_image = MagicMock(return_value=None)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
