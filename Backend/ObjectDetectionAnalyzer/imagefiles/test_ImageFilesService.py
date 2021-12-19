from unittest import TestCase
from unittest.mock import patch

from ObjectDetectionAnalyzer.imagefiles.ImageFilesService import ImageFilesService


class TestImageFilesService(TestCase):
    """
    Test ImageFilesService
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
