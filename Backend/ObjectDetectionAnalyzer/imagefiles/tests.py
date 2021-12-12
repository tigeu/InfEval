from unittest import TestCase
from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.imagefiles.services import ImageFilesService


class test_image_files(APITestCase):
    """
    Test image files app
    """

    def setUp(self):
        self.url = reverse('image-files')
        self.files = ["file1.jpg", "file2.png", "file3.jpg"]

    @patch('ObjectDetectionAnalyzer.imagefiles.services.ImageFilesService.get_image_file_names')
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

    @patch('ObjectDetectionAnalyzer.imagefiles.services.ImageFilesService.get_image_file_names')
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


class test_image_files_service(TestCase):
    """
    Test FileService.py in module services
    """

    def setUp(self):
        self.image_files_service = ImageFilesService()
        self.directory = "sample/directory/"
        self.image_endings = {".jpg", ".png"}

    @patch("os.listdir")
    @patch("os.path.exists")
    def test_image_file_names_with_data(self, path_exists, listdir):
        files = ["file1.jpg", "file2.png", "file3.xxx"]
        path_exists.return_value = True
        listdir.return_value = files

        file_names = self.image_files_service.get_image_file_names(self.directory, self.image_endings)

        self.assertEqual(file_names, ["file1.jpg", "file2.png"])

    @patch("os.listdir")
    @patch("os.path.exists")
    def test_image_file_names_without_data(self, path_exists, listdir):
        files = []
        path_exists.return_value = True
        listdir.return_value = files

        file_names = self.image_files_service.get_image_file_names(self.directory, self.image_endings)

        self.assertEqual(file_names, [])

    @patch("os.path.exists")
    def test_image_file_names_with_wrong_directory(self, path_exists):
        path_exists.return_value = False

        file_names = self.image_files_service.get_image_file_names(self.directory, self.image_endings)

        self.assertEqual(file_names, None)
