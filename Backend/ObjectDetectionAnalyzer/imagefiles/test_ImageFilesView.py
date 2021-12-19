from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestImageFilesView(APITestCase):
    """
    Test ImageFilesView
    """

    def setUp(self):
        self.url = reverse('image-files')
        self.files = ["file1.jpg", "file2.png", "file3.jpg"]

    @patch('ObjectDetectionAnalyzer.imagefiles.ImageFilesService.ImageFilesService.get_image_file_names')
    def test_image_files_with_data(self, get_image_file_names):
        """
        Test that correct image is returned
        """
        get_image_file_names.return_value = self.files

        user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], "file1.jpg")
        self.assertEqual(response.data[1]['name'], "file2.png")
        self.assertEqual(response.data[2]['name'], "file3.jpg")

    @patch('ObjectDetectionAnalyzer.imagefiles.ImageFilesService.ImageFilesService.get_image_file_names')
    def test_image_files_without_data(self, get_image_file_names):
        """
        Test that 404 not found is returned
        """
        get_image_file_names.return_value = []

        user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_authentication_image_files(self):
        """
        Test that user without authentication gets 401
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
