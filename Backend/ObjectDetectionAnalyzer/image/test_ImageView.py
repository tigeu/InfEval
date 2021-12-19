from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestImageView(APITestCase):
    """
    Test ImageView
    """

    def setUp(self):
        self.url = reverse('image', kwargs={'image_name': "test_image.jpg"})

    @patch('ObjectDetectionAnalyzer.image.ImageService.ImageService.encode_image')
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

    @patch('ObjectDetectionAnalyzer.image.ImageService.ImageService.encode_image')
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
