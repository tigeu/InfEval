from unittest import TestCase
from unittest.mock import patch

from ObjectDetectionAnalyzer.upload.validators.LabelMapValidator import LabelMapValidator


class TestLabelMapValidator(TestCase):
    """
    Test LabelMapValidator
    """

    def setUp(self):
        self.validator = LabelMapValidator()

    @patch('ObjectDetectionAnalyzer.services.JSONService.JSONService.read_label_map')
    def test_is_valid(self, read_label_map):
        read_label_map.return_value = {"1": "class1", "2": "class2", "3": "class3"}

        result = self.validator.is_valid("file_path")

        self.assertEqual(result, True)

    @patch('ObjectDetectionAnalyzer.services.JSONService.JSONService.read_label_map')
    def test_is_valid_without_values(self, get_values):
        get_values.return_value = {}

        result = self.validator.is_valid("file_path")

        self.assertEqual(result, False)

    def test_is_valid_with_exception(self):
        result = self.validator.is_valid("file_path")

        self.assertEqual(result, False)
