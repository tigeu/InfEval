import io
from unittest import TestCase
from unittest.mock import patch

import PIL.PngImagePlugin

from ObjectDetectionAnalyzer.upload.validators.YoloValidator import YoloValidator


class TestYoloValidator(TestCase):
    """
    Test YoloValidator
    """

    def setUp(self):
        self.validator = YoloValidator()

    @patch('ObjectDetectionAnalyzer.upload.validators.YoloValidator.YoloValidator._create_test_image')
    @patch('ObjectDetectionAnalyzer.services.YoloService.YoloService.get_detections_for_images')
    def test_is_valid(self, get_detections_for_images, create_test_image):
        get_detections_for_images.return_value = []
        create_test_image.return_value = io.BytesIO()

        result = self.validator.is_valid("file_path", "yolo_dir")

        self.assertEqual(result, True)

    @patch('ObjectDetectionAnalyzer.upload.validators.YoloValidator.YoloValidator._create_test_image')
    def test_is_valid_exception(self, create_test_image):
        create_test_image.return_value = io.BytesIO()

        result = self.validator.is_valid("file_path", "yolo_dir")

        self.assertEqual(result, False)

    def test_create_test_image(self):
        result = self.validator._create_test_image()

        self.assertIsInstance(result, PIL.PngImagePlugin.PngImageFile)
