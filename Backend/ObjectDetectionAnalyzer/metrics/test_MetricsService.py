from unittest import TestCase

from ObjectDetectionAnalyzer.metrics.MetricsService import MetricsService


class TestMetricService(TestCase):
    """
    Test MetricService
    """

    def setUp(self):
        self.metric_service = MetricsService()

    def test_pascal_voc(self):
        gts = {"image": [
            {'class': 'class1', 'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10},
            {'class': 'class1', 'xmin': 20, 'xmax': 30, 'ymin': 20, 'ymax': 30},
            {'class': 'class2', 'xmin': 50, 'xmax': 60, 'ymin': 50, 'ymax': 60}
        ]}
        predictions = {"image": [
            {'class': 'class1', 'confidence': 0.9, 'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10},
            {'class': 'class1', 'confidence': 0.9, 'xmin': 30, 'xmax': 40, 'ymin': 20, 'ymax': 30},
            {'class': 'class2', 'confidence': 0.9, 'xmin': 60, 'xmax': 70, 'ymin': 50, 'ymax': 60}
        ]}

        result = self.metric_service.calculate_pascal_voc(gts, predictions, 0.5, ['class1', 'class2'])

        print(result)

    def test_coco(self):
        gts = {"image": [
            {'class': 'class1', 'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10},
            {'class': 'class1', 'xmin': 20, 'xmax': 30, 'ymin': 20, 'ymax': 30},
            {'class': 'class2', 'xmin': 50, 'xmax': 60, 'ymin': 50, 'ymax': 60}
        ]}
        predictions = {"image": [
            {'class': 'class1', 'confidence': 0.9, 'xmin': 0, 'xmax': 10, 'ymin': 0, 'ymax': 10},
            {'class': 'class1', 'confidence': 0.9, 'xmin': 30, 'xmax': 40, 'ymin': 20, 'ymax': 30},
            {'class': 'class2', 'confidence': 0.9, 'xmin': 60, 'xmax': 70, 'ymin': 50, 'ymax': 60}
        ]}

        result = self.metric_service.calculate_coco(gts, predictions, ['class1', 'class2'])

        print(result)
