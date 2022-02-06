import io
from unittest import TestCase
from unittest.mock import patch

from ObjectDetectionAnalyzer.services.JSONService import JSONService


@patch('builtins.open')
class TestJSONService(TestCase):
    """
    Test JSONService
    """

    def setUp(self):
        self.json_service = JSONService()
        self.indices = {'file_name': 0, 'class': 1, 'confidence': 2, 'xmin': 3, 'ymin': 4, 'xmax': 5, 'ymax': 6}
        self.json_file = io.StringIO(
            '{"1": "class1", "2": "class2", "3": "class3"}'
        )

    def test_read_label_map(self, open):
        open.return_value = self.json_file
        values = self.json_service.read_label_map(self.json_file)
        expected = {
            "1": "class1",
            "2": "class2",
            "3": "class3",
        }

        self.assertEqual(values, expected)
