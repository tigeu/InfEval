import os
from unittest.mock import MagicMock, patch, mock_open

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.image.services import ImageService


class test_image(APITestCase):
    """
    Test Image app
    """

    def __init__(self, methodName='runTest'):
        super(test_image, self).__init__(methodName)

        self.url = reverse('image', kwargs={'image_name': "test_image.jpg"})

    def test_image_with_data(self):
        """
        Test that correct image is returned
        """
        ImageService.encode_image = MagicMock(return_value=["dGVzdA=="])

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "test_image.jpg")
        self.assertEqual(response.data['file'], "['dGVzdA==']")

    def test_image_without_data(self):
        """
        Test that 404 not found is returned
        """
        ImageService.encode_image = MagicMock(return_value=None)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class test_image_service(APITestCase):
    """
    Test image service
    """

    def __init__(self, methodName='runTest'):
        super(test_image_service, self).__init__(methodName)
        self.image_service = ImageService()
        self.directory = "sample/directory/"

    def test_encode_image_with_data(self):
        os.path.exists = MagicMock(return_value=True)

        with patch("builtins.open", mock_open(read_data=b"test")) as mock:
            encoded_file = self.image_service.encode_image("file1.jpg")

        self.assertEqual(encoded_file, "dGVzdA==")

    def test_encode_image_with_wrong_directory(self):
        os.path.exists = MagicMock(return_value=False)

        encoded_file = self.image_service.encode_image("file1.jpg")

        self.assertEqual(encoded_file, None)
