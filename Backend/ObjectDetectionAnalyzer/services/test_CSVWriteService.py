import csv
import os
from unittest import TestCase

from ObjectDetectionAnalyzer.services.CSVWriteService import CSVWriteService


class TestCSVWriteService(TestCase):
    """
    Test CSVWriteService
    """

    def setUp(self):
        self.csv_write_service = CSVWriteService()
        self.detections = {"some_path": [{'class': 'class1', 'confidence': 0.5,
                                          'xmin': 0, 'ymin': 0, 'xmax': 100, 'ymax': 50}]}

    # seems impossible to mock csv writer, so create file and delete afterwards
    def test_get_values(self):
        self.csv_write_service.write_predictions(self.detections, "tmp_test_file")
        with open("tmp_test_file", "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            for row in reader:
                self.assertEqual(row, ['some_path', 'class1', '0.5', '0', '0', '100', '50'])

        os.remove("tmp_test_file")
