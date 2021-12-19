from unittest import TestCase
from unittest.mock import patch, mock_open

from ObjectDetectionAnalyzer.image.ImageService import ImageService


class TestImageService(TestCase):
    """
    Test ImageService
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
