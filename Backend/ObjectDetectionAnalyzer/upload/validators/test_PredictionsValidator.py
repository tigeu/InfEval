from unittest import TestCase
from unittest.mock import patch

from ObjectDetectionAnalyzer.upload.validators.PredictionsValidator import PredictionsValidator


class TestPredictionsValidator(TestCase):
    """
    Test PredictionsValidator
    """

    def setUp(self):
        self.validator = PredictionsValidator()

    @patch('ObjectDetectionAnalyzer.services.CSVParseService.CSVParseService.get_values')
    def test_is_valid(self, get_values):
        get_values.return_value = {"file": [{"value"}]}

        result = self.validator.is_valid("file_path")

        self.assertEqual(result, True)

    @patch('ObjectDetectionAnalyzer.services.CSVParseService.CSVParseService.get_values')
    def test_is_valid_without_values(self, get_values):
        get_values.return_value = {}

        result = self.validator.is_valid("file_path")

        self.assertEqual(result, False)

    def test_is_valid_with_exception(self):
        result = self.validator.is_valid("file_path")

        self.assertEqual(result, False)
