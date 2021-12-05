from unittest.mock import MagicMock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.main.services.FileService import FileService


class test_image_files(APITestCase):
    """
    Test Files.py
    """

    def __init__(self, methodName='runTest'):
        super(test_image_files, self).__init__(methodName)

        self.url = reverse('image-files')
        self.files = ["file1.jpg", "file2.png", "file3.jpg"]

    def test_image_files_with_data(self):
        """
        Test that correct image is returned
        """
        FileService.get_image_file_names = MagicMock(return_value=self.files)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], "file1.jpg")
        self.assertEqual(response.data[1]['name'], "file2.png")
        self.assertEqual(response.data[2]['name'], "file3.jpg")

    def test_image_files_without_data(self):
        """
        Test that 404 not found is returned
        """
        FileService.get_image_file_names = MagicMock(return_value=[])

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
