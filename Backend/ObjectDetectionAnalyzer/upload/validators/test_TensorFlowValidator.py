import io
from unittest import TestCase
from unittest.mock import patch

from ObjectDetectionAnalyzer.upload.validators.TensorFlowValidator import TensorFlowValidator


class TestTensorFlowValidator(TestCase):
    """
    Test TensorFlowValidator
    """

    def setUp(self):
        self.validator = TensorFlowValidator()

    @patch('ObjectDetectionAnalyzer.upload.validators.TensorFlowValidator.TensorFlowValidator._create_test_image')
    @patch('ObjectDetectionAnalyzer.services.TensorFlowService.TensorFlowService.get_detections_for_images')
    def test_is_valid(self, get_detections_for_images, create_test_image):
        get_detections_for_images.return_value = []
        create_test_image.return_value = io.BytesIO()

        result = self.validator.is_valid("file_path", True)

        self.assertEqual(result, True)

    @patch('ObjectDetectionAnalyzer.upload.validators.TensorFlowValidator.TensorFlowValidator._create_test_image')
    def test_is_valid_exception(self, create_test_image):
        create_test_image.return_value = io.BytesIO()

        result = self.validator.is_valid("file_path", False)

        self.assertEqual(result, False)

    def test_create_test_image(self):
        result = self.validator._create_test_image()

        self.assertIsInstance(result, io.BytesIO)
