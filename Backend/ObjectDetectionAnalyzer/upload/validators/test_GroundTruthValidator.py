from unittest import TestCase
from unittest.mock import patch

from ObjectDetectionAnalyzer.upload.validators.GroundTruthValidator import GroundTruthValidator


class TestGroundTruthValidator(TestCase):
    """
    Test GroundTruthValidator
    """

    def setUp(self):
        self.validator = GroundTruthValidator()

    @patch('ObjectDetectionAnalyzer.services.CSVParseService.CSVParseService.get_values')
    def test_is_valid(self, get_values):
        get_values.return_value = [{"file": [{"value"}]}]

        result = self.validator.is_valid("file_path")

        self.assertEqual(result, [{"file": [{"value"}]}])

    @patch('ObjectDetectionAnalyzer.services.CSVParseService.CSVParseService.get_values')
    def test_is_valid_without_values(self, get_values):
        get_values.return_value = {}

        result = self.validator.is_valid("file_path")

        self.assertEqual(result, [])

    def test_is_valid_with_exception(self):
        result = self.validator.is_valid("file_path")

        self.assertEqual(result, [])
