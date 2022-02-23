from unittest import TestCase

from ObjectDetectionAnalyzer.services.FilterPredictionsService import FilterPredictionsService


class TestNMSService(TestCase):
    """
    Test NMSService
    """

    def setUp(self):
        self.filter_predictions_service = FilterPredictionsService()

    def test_get_interval_predictions(self):
        predictions = [
            {'class': 1, 'confidence': 0.9, 'xmin': 50, 'ymin': 20, 'xmax': 60, 'ymax': 30},
            {'class': 2, 'confidence': 0.6, 'xmin': 10, 'ymin': 60, 'xmax': 90, 'ymax': 100},
            {'class': 1, 'confidence': 0.7, 'xmin': 49, 'ymin': 20, 'xmax': 61, 'ymax': 30},
            {'class': 2, 'confidence': 0.6, 'xmin': 20, 'ymin': 60, 'xmax': 50, 'ymax': 100},
            {'class': 1, 'confidence': 0.1, 'xmin': 400, 'ymin': 200, 'xmax': 700, 'ymax': 300},
            {'class': 2, 'confidence': 0.6, 'xmin': 200, 'ymin': 600, 'xmax': 500, 'ymax': 1000},
        ]

        expected = [
            {'class': 2, 'confidence': 0.6, 'xmin': 10, 'ymin': 60, 'xmax': 90, 'ymax': 100},
            {'class': 1, 'confidence': 0.7, 'xmin': 49, 'ymin': 20, 'xmax': 61, 'ymax': 30},
            {'class': 2, 'confidence': 0.6, 'xmin': 20, 'ymin': 60, 'xmax': 50, 'ymax': 100},
            {'class': 2, 'confidence': 0.6, 'xmin': 200, 'ymin': 600, 'xmax': 500, 'ymax': 1000},
        ]

        nms_predictions = self.filter_predictions_service.get_interval_predictions(predictions, 0.5, 0.8)

        self.assertEqual(nms_predictions, expected)

    def test_get_interval_predictions_without_predictions(self):
        predictions = [
            {'class': 1, 'confidence': 0.9, 'xmin': 50, 'ymin': 20, 'xmax': 60, 'ymax': 30},
            {'class': 2, 'confidence': 0.6, 'xmin': 10, 'ymin': 60, 'xmax': 90, 'ymax': 100},
            {'class': 1, 'confidence': 0.7, 'xmin': 49, 'ymin': 20, 'xmax': 61, 'ymax': 30},
            {'class': 2, 'confidence': 0.6, 'xmin': 20, 'ymin': 60, 'xmax': 50, 'ymax': 100},
            {'class': 1, 'confidence': 0.1, 'xmin': 400, 'ymin': 200, 'xmax': 700, 'ymax': 300},
            {'class': 2, 'confidence': 0.6, 'xmin': 200, 'ymin': 600, 'xmax': 500, 'ymax': 1000},
        ]

        expected = []

        nms_predictions = self.filter_predictions_service.get_interval_predictions(predictions, 0.2, 0.3)

        self.assertEqual(nms_predictions, expected)

    def test_get_nms_predictions(self):
        predictions = [
            {'class': 1, 'confidence': 0.9, 'xmin': 50, 'ymin': 20, 'xmax': 60, 'ymax': 30},
            {'class': 2, 'confidence': 0.6, 'xmin': 10, 'ymin': 60, 'xmax': 90, 'ymax': 100},
            {'class': 1, 'confidence': 0.7, 'xmin': 49, 'ymin': 20, 'xmax': 61, 'ymax': 30},
            {'class': 2, 'confidence': 0.6, 'xmin': 20, 'ymin': 60, 'xmax': 50, 'ymax': 100},
            {'class': 1, 'confidence': 0.1, 'xmin': 400, 'ymin': 200, 'xmax': 700, 'ymax': 300},
            {'class': 2, 'confidence': 0.6, 'xmin': 200, 'ymin': 600, 'xmax': 500, 'ymax': 1000},
        ]

        expected = [
            {'class': 1, 'confidence': 0.9, 'xmin': 50, 'ymin': 20, 'xmax': 60, 'ymax': 30},
            {'class': 2, 'confidence': 0.6, 'xmin': 10, 'ymin': 60, 'xmax': 90, 'ymax': 100},
            {'class': 2, 'confidence': 0.6, 'xmin': 20, 'ymin': 60, 'xmax': 50, 'ymax': 100},
            {'class': 2, 'confidence': 0.6, 'xmin': 200, 'ymin': 600, 'xmax': 500, 'ymax': 1000},
        ]

        nms_predictions = self.filter_predictions_service.get_nms_predictions(predictions, 0.5, 0.5)

        self.assertEqual(nms_predictions, expected)

    def test_get_nms_predictions_without_result(self):
        predictions = [
            {'class': 1, 'confidence': 0.5, 'xmin': 50, 'ymin': 20, 'xmax': 60, 'ymax': 30},
            {'class': 2, 'confidence': 0.5, 'xmin': 10, 'ymin': 60, 'xmax': 90, 'ymax': 100},
            {'class': 1, 'confidence': 0.3, 'xmin': 49, 'ymin': 20, 'xmax': 61, 'ymax': 30},
            {'class': 2, 'confidence': 0.2, 'xmin': 20, 'ymin': 60, 'xmax': 50, 'ymax': 100},
            {'class': 1, 'confidence': 0.1, 'xmin': 400, 'ymin': 200, 'xmax': 700, 'ymax': 300},
            {'class': 2, 'confidence': 0.05, 'xmin': 200, 'ymin': 600, 'xmax': 500, 'ymax': 1000},
        ]

        nms_predictions = self.filter_predictions_service.get_nms_predictions(predictions, 0.5, 0.5)

        self.assertEqual(nms_predictions, [])

    def test_get_nms_predictions_without_predictions(self):
        predictions = []

        nms_predictions = self.filter_predictions_service.get_nms_predictions(predictions, 0.5, 0.5)

        self.assertEqual(nms_predictions, [])
