from unittest import TestCase
from unittest.mock import patch

from numpy import nan
from src.bounding_box import BoundingBox

from ObjectDetectionAnalyzer.metrics.MetricsService import MetricsService
from metric.review_object_detection_metrics.src.utils.enumerators import CoordinatesType, BBType, BBFormat


class TestMetricService(TestCase):
    """
    Test MetricService
    """

    def setUp(self):
        self.metric_service = MetricsService()

    @patch('ObjectDetectionAnalyzer.metrics.MetricsService.MetricsService._get_overall_positives')
    @patch('ObjectDetectionAnalyzer.metrics.MetricsService.MetricsService._extract_results_per_class')
    @patch('src.evaluators.pascal_voc_evaluator.get_pascalvoc_metrics')
    @patch('ObjectDetectionAnalyzer.metrics.MetricsService.MetricsService._convert_predictions')
    @patch('ObjectDetectionAnalyzer.metrics.MetricsService.MetricsService._convert_ground_truths')
    def test_calculate_pascal(self, convert_ground_truths, convert_predictions, get_pascalvoc_metrics,
                              extract_results_per_class, get_overall_positives):
        gts = ["gt1", "gt2"]
        preds = ["pred1", "pred2"]
        convert_ground_truths.return_value = gts
        convert_predictions.return_value = preds
        get_pascalvoc_metrics.return_value = {"mAP": 0.5, 'per_class': {}}
        extract_results_per_class.return_value = {'class1': 'value1'}
        get_overall_positives.return_value = (5, 5, 5)

        results = self.metric_service.calculate_pascal_voc(gts, preds, 0.5, [])

        self.assertEqual(results, {"mAP": 50.0,
                                   'classes': {'class1': 'value1'},
                                   'precision': 100.0,
                                   'recall': 50.0,
                                   'positives': 5,
                                   'TP': 5,
                                   'FP': 5})

    @patch('ObjectDetectionAnalyzer.metrics.MetricsService.MetricsService._get_overall_positives')
    @patch('ObjectDetectionAnalyzer.metrics.MetricsService.MetricsService._extract_coco_summary')
    @patch('ObjectDetectionAnalyzer.metrics.MetricsService.MetricsService._extract_results_per_class')
    @patch('src.evaluators.coco_evaluator.get_coco_metrics')
    @patch('src.evaluators.coco_evaluator.get_coco_summary')
    @patch('ObjectDetectionAnalyzer.metrics.MetricsService.MetricsService._convert_predictions')
    @patch('ObjectDetectionAnalyzer.metrics.MetricsService.MetricsService._convert_ground_truths')
    def test_calculate_coco(self, convert_ground_truths, convert_predictions, get_coco_summary, get_coco_metrics,
                            extract_results_per_class, extract_coco_summary, get_overall_positives):
        gts = ["gt1", "gt2"]
        preds = ["pred1", "pred2"]
        convert_ground_truths.return_value = gts
        convert_predictions.return_value = preds
        get_coco_metrics.return_value = {"mAP": 0.5, 'per_class': {}}
        extract_results_per_class.return_value = {'class1': 'value1'}
        extract_coco_summary.return_value = {'coco': 'summary'}
        get_overall_positives.return_value = (5, 5, 5)

        results = self.metric_service.calculate_coco(gts, preds, [])

        self.assertEqual(results, {"summary": {'coco': 'summary'},
                                   'classes': {'class1': 'value1'},
                                   'precision': 100.0,
                                   'recall': 50.0,
                                   'positives': 5,
                                   'TP': 5,
                                   'FP': 5})

    def test_extract_results_per_class_pascal(self):
        classes = ['class1', 'class2', 'class3']
        metrics = {'class1': {'AP': 0.12345, 'total positives': 5, 'total TP': 3, 'total FP': 3},
                   'class2': {'AP': 0.98765, 'total positives': 0, 'total TP': 0, 'total FP': 0}}

        expected = {'class1': {'AP': 12.35, 'precision': 50.0, 'recall': 60.0, 'positives': 5, 'TP': 3, 'FP': 3},
                    'class2': {'AP': 98.77, 'precision': -1, 'recall': -1, 'positives': 0, 'TP': 0, 'FP': 0}}

        results = self.metric_service._extract_results_per_class(classes, metrics)

        self.assertEqual(results, expected)

    def test_extract_results_per_class_coco(self):
        classes = ['class1', 'class2', 'class3']
        metrics = {'class1': {'AP': 0.12345, 'total positives': 5, 'TP': 3, 'FP': 3},
                   'class2': {'AP': 0.98765, 'total positives': 0, 'TP': 0, 'FP': 0}}

        expected = {'class1': {'AP': 12.35, 'precision': 50.0, 'recall': 60.0, 'positives': 5, 'TP': 3, 'FP': 3},
                    'class2': {'AP': 98.77, 'precision': -1, 'recall': -1, 'positives': 0, 'TP': 0, 'FP': 0}}

        results = self.metric_service._extract_results_per_class(classes, metrics, True)

        self.assertEqual(results, expected)

    def test_get_overall_positives(self):
        classes = {'class1': {'TP': 5, 'FP': 5, 'positives': 5},
                   'class2': {'TP': 0, 'FP': 2, 'positives': 1}}

        results = self.metric_service._get_overall_positives(classes)

        self.assertEqual(results, (5, 7, 6))

    def test_create_coco_summary(self):
        summary = {"key": 0.12345, "key2": 0.98765, "key3": nan}
        expected = {"key": 12.35, "key2": 98.77, "key3": -1}

        results = self.metric_service._extract_coco_summary(summary)

        self.assertEqual(results, expected)

    def test_convert_ground_truths(self):
        ground_truths = [
            {'class': 'class1', 'file_name': 'file1.jpg', 'xmin': 0, 'ymin': 0, 'xmax': 100, 'ymax': 100},
            {'class': 'class1', 'file_name': 'file2.png', 'xmin': 25, 'ymin': 25, 'xmax': 100, 'ymax': 100}
        ]
        expected = [
            BoundingBox(image_name="file1.jpg", class_id="class1", coordinates=(0, 0, 100, 100),
                        type_coordinates=CoordinatesType.ABSOLUTE, bb_type=BBType.GROUND_TRUTH, format=BBFormat.XYX2Y2),
            BoundingBox(image_name="file2.png", class_id="class1", coordinates=(25, 25, 100, 100),
                        type_coordinates=CoordinatesType.ABSOLUTE, bb_type=BBType.GROUND_TRUTH, format=BBFormat.XYX2Y2)
        ]
        results = self.metric_service._convert_ground_truths(ground_truths)

        self.assertEqual(results[0], expected[0])
        self.assertEqual(results[1], expected[1])

    def test_convert_predictions(self):
        predictions = [
            {'class': 'class1', 'confidence': 55, 'file_name': 'file1.jpg', 'xmin': 0, 'ymin': 0, 'xmax': 100,
             'ymax': 100},
            {'class': 'class1', 'confidence': 43, 'file_name': 'file2.png', 'xmin': 25, 'ymin': 25, 'xmax': 100,
             'ymax': 100}
        ]
        expected = [
            BoundingBox(image_name="file1.jpg", class_id="class1", confidence=55, coordinates=(0, 0, 100, 100),
                        type_coordinates=CoordinatesType.ABSOLUTE, bb_type=BBType.DETECTED, format=BBFormat.XYX2Y2),
            BoundingBox(image_name="file2.png", class_id="class1", confidence=43, coordinates=(25, 25, 100, 100),
                        type_coordinates=CoordinatesType.ABSOLUTE, bb_type=BBType.DETECTED, format=BBFormat.XYX2Y2)
        ]
        results = self.metric_service._convert_predictions(predictions)

        self.assertEqual(results[0], expected[0])
        self.assertEqual(results[1], expected[1])

    def test_get_percent(self):
        result = self.metric_service._get_percent(0.123456789)

        self.assertEqual(result, 12.35)
