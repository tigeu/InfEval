import os
from unittest.mock import MagicMock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.imagefiles.services import ImageFilesService


class test_image_files(APITestCase):
    """
    Test image files app
    """

    def __init__(self, methodName='runTest'):
        super(test_image_files, self).__init__(methodName)

        self.url = reverse('image-files')
        self.files = ["file1.jpg", "file2.png", "file3.jpg"]

    def test_image_files_with_data(self):
        """
        Test that correct image is returned
        """
        ImageFilesService.get_image_file_names = MagicMock(return_value=self.files)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], "file1.jpg")
        self.assertEqual(response.data[1]['name'], "file2.png")
        self.assertEqual(response.data[2]['name'], "file3.jpg")

    def test_image_files_without_data(self):
        """
        Test that 404 not found is returned
        """
        ImageFilesService.get_image_file_names = MagicMock(return_value=[])

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class test_image_files_service(APITestCase):
    """
    Test FileService.py in module services
    """

    def __init__(self, methodName='runTest'):
        super(test_image_files_service, self).__init__(methodName)
        self.image_files_service = ImageFilesService()
        self.directory = "sample/directory/"
        self.image_endings = {".jpg", ".png"}

    def test_image_file_names_with_data(self):
        files = ["file1.jpg", "file2.png", "file3.xxx"]
        os.path.exists = MagicMock(return_value=True)
        os.listdir = MagicMock(return_value=files)

        file_names = self.image_files_service.get_image_file_names(self.directory, self.image_endings)

        self.assertEqual(file_names, ["file1.jpg", "file2.png"])

    def test_image_file_names_without_data(self):
        files = []
        os.path.exists = MagicMock(return_value=True)
        os.listdir = MagicMock(return_value=files)

        file_names = self.image_files_service.get_image_file_names(self.directory, self.image_endings)

        self.assertEqual(file_names, [])

    def test_image_file_names_with_wrong_directory(self):
        os.path.exists = MagicMock(return_value=False)

        file_names = self.image_files_service.get_image_file_names(self.directory, self.image_endings)

        self.assertEqual(file_names, None)
