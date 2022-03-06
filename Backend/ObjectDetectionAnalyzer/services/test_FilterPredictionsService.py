from unittest import TestCase

from ObjectDetectionAnalyzer.services.FilterPredictionsService import FilterPredictionsService


class TestFilterPredictionsService(TestCase):
    """
    Test FilterPredictionsService
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

    def test_get_ground_truth_results_identical(self):
        gts = [{'class': 'class1', 'confidence': 0.9, 'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10},
               {'class': 'class1', 'confidence': 0.9, 'xmin': 20, 'xmax': 30, 'ymin': 20, 'ymax': 30},
               {'class': 'class2', 'confidence': 0.9, 'xmin': 50, 'xmax': 60, 'ymin': 50, 'ymax': 60}]
        predictions = gts
        expected = [
            {'matched': True, 'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10},
            {'matched': True, 'xmin': 20, 'xmax': 30, 'ymin': 20, 'ymax': 30},
            {'matched': True, 'xmin': 50, 'xmax': 60, 'ymin': 50, 'ymax': 60}
        ]

        results = self.filter_predictions_service.get_ground_truth_results(gts, predictions, 0.5)

        self.assertEqual(results, expected)

    def test_get_ground_truth_results_no_matches(self):
        gts = [{'class': 'class1', 'confidence': 0.9, 'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10},
               {'class': 'class1', 'confidence': 0.9, 'xmin': 20, 'xmax': 30, 'ymin': 20, 'ymax': 30},
               {'class': 'class2', 'confidence': 0.9, 'xmin': 50, 'xmax': 60, 'ymin': 50, 'ymax': 60}]
        predictions = [{'class': 'class1', 'confidence': 0.9, 'xmin': 10, 'xmax': 20, 'ymin': 0, 'ymax': 10},
                       {'class': 'class1', 'confidence': 0.9, 'xmin': 30, 'xmax': 40, 'ymin': 20, 'ymax': 30},
                       {'class': 'class2', 'confidence': 0.9, 'xmin': 60, 'xmax': 70, 'ymin': 50, 'ymax': 60}]
        expected = [{'matched': False, 'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10},
                    {'matched': False, 'xmin': 20, 'xmax': 30, 'ymin': 20, 'ymax': 30},
                    {'matched': False, 'xmin': 50, 'xmax': 60, 'ymin': 50, 'ymax': 60}]

        results = self.filter_predictions_service.get_ground_truth_results(gts, predictions, 0.5)

        self.assertEqual(results, expected)

    def test_get_ground_truth_results(self):
        gts = [{'class': 'class1', 'confidence': 0.9, 'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10},
               {'class': 'class1', 'confidence': 0.9, 'xmin': 20, 'xmax': 30, 'ymin': 20, 'ymax': 30},
               {'class': 'class2', 'confidence': 0.9, 'xmin': 50, 'xmax': 60, 'ymin': 50, 'ymax': 60}]
        predictions = [{'class': 'class1', 'confidence': 0.9, 'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10},
                       {'class': 'class1', 'confidence': 0.9, 'xmin': 30, 'xmax': 40, 'ymin': 20, 'ymax': 30},
                       {'class': 'class2', 'confidence': 0.9, 'xmin': 60, 'xmax': 70, 'ymin': 50, 'ymax': 60}]
        expected = [{'matched': True, 'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10},
                    {'matched': False, 'xmin': 20, 'xmax': 30, 'ymin': 20, 'ymax': 30},
                    {'matched': False, 'xmin': 50, 'xmax': 60, 'ymin': 50, 'ymax': 60}]

        results = self.filter_predictions_service.get_ground_truth_results(gts, predictions, 0.5)

        self.assertEqual(results, expected)

    def test_calculate_iou_top_left_bottom_right(self):
        box1 = {'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10}
        box2 = {'xmin': 5, 'xmax': 15, 'ymin': 5, 'ymax': 15}

        result = self.filter_predictions_service._calculate_iou(box1, box2)

        self.assertAlmostEqual(result, 0.1429, delta=0.001)

    def test_calculate_iou_top_right_bottom_left(self):
        box1 = {'xmin': 10, 'xmax': 20, 'ymin': 0, 'ymax': 10}
        box2 = {'xmin': 5, 'xmax': 15, 'ymin': 5, 'ymax': 15}

        result = self.filter_predictions_service._calculate_iou(box1, box2)

        self.assertAlmostEqual(result, 0.1429, delta=0.001)

    def test_calculate_iou_bottom_left_top_right(self):
        box1 = {'xmin': 0, 'xmax': 10, 'ymin': 10, 'ymax': 20}
        box2 = {'xmin': 5, 'xmax': 15, 'ymin': 5, 'ymax': 15}

        result = self.filter_predictions_service._calculate_iou(box1, box2)

        self.assertAlmostEqual(result, 0.1429, delta=0.001)

    def test_calculate_iou_identical(self):
        box1 = {'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10}
        box2 = {'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10}
        result = self.filter_predictions_service._calculate_iou(box1, box2)

        self.assertEqual(result, 1.0)

    def test_calculate_iou_next_to_each_other(self):
        box1 = {'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10}
        box2 = {'xmin': 10, 'xmax': 20, 'ymin': 10, 'ymax': 20}
        result = self.filter_predictions_service._calculate_iou(box1, box2)

        self.assertEqual(result, 0.0)

    def test_calculate_iou_not_overlapping(self):
        box1 = {'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10}
        box2 = {'xmin': 100, 'xmax': 200, 'ymin': 100, 'ymax': 200}
        result = self.filter_predictions_service._calculate_iou(box1, box2)

        self.assertEqual(result, 0.0)

    def test_calculate_iou_contains_other(self):
        box1 = {'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10}
        box2 = {'xmin': 2.5, 'xmax': 7.5, 'ymin': 2.5, 'ymax': 7.5}
        result = self.filter_predictions_service._calculate_iou(box1, box2)

        self.assertEqual(result, 0.25)
