import os
import unittest
from unittest.mock import MagicMock, patch, mock_open

from ObjectDetectionAnalyzer.main.services.FileService import FileService


class test_file_service(unittest.TestCase):
    """
    Test FileService.py in module services
    """

    def __init__(self, methodName='runTest'):
        super(test_file_service, self).__init__(methodName)
        self.file_service = FileService()
        self.directory = "sample/directory/"
        self.image_endings = {".jpg", ".png"}
        self.image_name = "test_image.jpg"

    def test_image_file_names_with_data(self):
        files = ["file1.jpg", "file2.png", "file3.xxx"]
        os.path.exists = MagicMock(return_value=True)
        os.listdir = MagicMock(return_value=files)

        file_names = self.file_service.get_image_file_names(self.directory, self.image_endings)

        self.assertEqual(file_names, ["file1.jpg", "file2.png"])

    def test_image_file_names_without_data(self):
        files = []
        os.path.exists = MagicMock(return_value=True)
        os.listdir = MagicMock(return_value=files)

        file_names = self.file_service.get_image_file_names(self.directory, self.image_endings)

        self.assertEqual(file_names, [])

    def test_image_file_names_with_wrong_directory(self):
        os.path.exists = MagicMock(return_value=False)

        file_names = self.file_service.get_image_file_names(self.directory, self.image_endings)

        self.assertEqual(file_names, None)

    def test_encode_image_with_data(self):
        os.path.exists = MagicMock(return_value=True)

        with patch("builtins.open", mock_open(read_data=b"test")) as mock:
            encoded_file = self.file_service.encode_image("file1.jpg")

        self.assertEqual(encoded_file, "dGVzdA==")

    def test_encode_image_with_wrong_directory(self):
        os.path.exists = MagicMock(return_value=False)

        encoded_file = self.file_service.encode_image("file1.jpg")

        self.assertEqual(encoded_file, None)
