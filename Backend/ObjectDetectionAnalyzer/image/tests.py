from unittest import TestCase
from unittest.mock import patch, mock_open

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.image.services import ImageService


class test_image(APITestCase):
    """
    Test Image app
    """

    def setUp(self):
        self.url = reverse('image', kwargs={'image_name': "test_image.jpg"})

    @patch('ObjectDetectionAnalyzer.image.services.ImageService.encode_image')
    def test_image_with_data(self, encode_image):
        """
        Test that correct image is returned
        """
        user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=user)

        encode_image.return_value = ["dGVzdA=="]

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "test_image.jpg")
        self.assertEqual(response.data['file'], "['dGVzdA==']")

    @patch('ObjectDetectionAnalyzer.image.services.ImageService.encode_image')
    def test_image_without_data(self, encode_image):
        """
        Test that 404 not found is returned
        """
        user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=user)

        encode_image.return_value = None

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_authentication_image(self):
        """
        Test that user without authentication gets 401
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class test_image_service(TestCase):
    """
    Test image service
    """

    def setUp(self):
        self.image_service = ImageService()
        self.directory = "sample/directory/"

    @patch("os.path.exists")
    def test_encode_image_with_data(self, path_exists):
        path_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=b"test")) as mock:
            encoded_file = self.image_service.encode_image("file1.jpg")

        self.assertEqual(encoded_file, "dGVzdA==")

    @patch("os.path.exists")
    def test_encode_image_with_wrong_directory(self, path_exists):
        path_exists.return_value = False

        encoded_file = self.image_service.encode_image("file1.jpg")

        self.assertEqual(encoded_file, None)
