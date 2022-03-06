import io
from unittest import TestCase
from unittest.mock import patch

from ObjectDetectionAnalyzer.upload.validators.PyTorchValidator import PyTorchValidator


class TestPyTorchValidator(TestCase):
    """
    Test PyTorchValidator
    """

    def setUp(self):
        self.validator = PyTorchValidator()

    @patch('ObjectDetectionAnalyzer.upload.validators.PyTorchValidator.PyTorchValidator._create_test_image')
    @patch('ObjectDetectionAnalyzer.services.PyTorchService.PyTorchService.get_detections_for_images')
    def test_is_valid(self, get_detections_for_images, create_test_image):
        get_detections_for_images.return_value = []
        create_test_image.return_value = io.BytesIO()

        result = self.validator.is_valid("file_path")

        self.assertEqual(result, True)

    @patch('ObjectDetectionAnalyzer.upload.validators.PyTorchValidator.PyTorchValidator._create_test_image')
    def test_is_valid_exception(self, create_test_image):
        create_test_image.return_value = io.BytesIO()

        result = self.validator.is_valid("file_path")

        self.assertEqual(result, False)

    def test_create_test_image(self):
        result = self.validator._create_test_image()

        self.assertIsInstance(result, io.BytesIO)
