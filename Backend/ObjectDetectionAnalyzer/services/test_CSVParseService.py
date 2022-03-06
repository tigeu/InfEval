import io
from unittest import TestCase
from unittest.mock import patch

from ObjectDetectionAnalyzer.services.CSVParseService import CSVParseService


@patch('builtins.open')
class TestCSVParseService(TestCase):
    """
    Test CSVParseService
    """

    def setUp(self):
        self.csv_parse_service = CSVParseService()
        self.indices = {'file_name': 0, 'class': 1, 'confidence': 2, 'xmin': 3, 'ymin': 4, 'xmax': 5, 'ymax': 6}
        self.csv_file = io.StringIO(
            "file1.jpg class1 0.55 0 0 100 100\n"
            "file2.png class1 0.43 25 25 100 100\n"
            "file2.png class2 0.67 100 100 101 101\n"
            "file2.png class3 0.1 50 50 100 100\n"
        )
        self.invalid_file = io.StringIO("")
        self.invalid_csv_file = io.StringIO("file1.jpg 0 class")

    def test_get_values(self, open):
        open.return_value = self.csv_file
        values = self.csv_parse_service.get_values(self.csv_file, self.indices)
        expected = [
            {'class': 'class1', 'confidence': 55, 'file_name': 'file1.jpg', 'xmin': 0, 'ymin': 0, 'xmax': 100,
             'ymax': 100},
            {'class': 'class1', 'confidence': 43, 'file_name': 'file2.png', 'xmin': 25, 'ymin': 25, 'xmax': 100,
             'ymax': 100},
            {'class': 'class2', 'confidence': 67, 'file_name': 'file2.png', 'xmin': 100, 'ymin': 100, 'xmax': 101,
             'ymax': 101},
            {'class': 'class3', 'confidence': 10, 'file_name': 'file2.png', 'xmin': 50, 'ymin': 50, 'xmax': 100,
             'ymax': 100}]

        self.assertEqual(values, expected)

    def test_get_values_for_image_with_one_prediction(self, open):
        open.return_value = self.csv_file
        values = self.csv_parse_service.get_values_for_image(self.csv_file, "file1.jpg", self.indices)
        expected = [{'class': 'class1', 'confidence': 55, 'file_name': 'file1.jpg', 'xmin': 0, 'ymin': 0, 'xmax': 100,
                     'ymax': 100}]

        self.assertEqual(values, expected)

    def test_get_values_for_image_with_several_predictions(self, open):
        open.return_value = self.csv_file
        values = self.csv_parse_service.get_values_for_image(self.csv_file, "file2.png", self.indices)
        expected = [{'class': 'class1', 'confidence': 43, 'file_name': 'file2.png', 'xmin': 25, 'ymin': 25, 'xmax': 100,
                     'ymax': 100},
                    {'class': 'class2', 'confidence': 67, 'file_name': 'file2.png', 'xmin': 100, 'ymin': 100,
                     'xmax': 101, 'ymax': 101},
                    {'class': 'class3', 'confidence': 10, 'file_name': 'file2.png', 'xmin': 50, 'ymin': 50, 'xmax': 100,
                     'ymax': 100}]

        self.assertEqual(values, expected)

    def test_get_values_for_image_with_invalid_file(self, open):
        open.return_value = self.invalid_file
        values = self.csv_parse_service.get_values_for_image(self.invalid_file, "file1.jpg", self.indices)

        self.assertEqual(values, [])

    def test_get_value(self, open):
        row = ['file1.jpg', 'class1', 0.55, 0, 0, 100, 100]
        value = self.csv_parse_service._get_value(row, self.indices)

        self.assertEqual(value, {'class': 'class1', 'confidence': 55, 'file_name': 'file1.jpg', 'xmin': 0, 'ymin': 0,
                                 'xmax': 100, 'ymax': 100})

    def test_get_classes(self, open):
        open.return_value = self.csv_file
        classes = self.csv_parse_service.get_classes(self.csv_file, 1)

        self.assertEqual(classes, ['class1', 'class2', 'class3'])

    def test_get_classes_with_invalid_file(self, open):
        open.return_value = self.invalid_file
        classes = self.csv_parse_service.get_classes(self.invalid_file, 1)

        self.assertEqual(classes, [])

    def test_get_classes_with_invalid_csv_file(self, open):
        open.return_value = self.invalid_csv_file
        classes = self.csv_parse_service.get_classes(self.invalid_csv_file, 1)

        self.assertEqual(classes, ['0'])
