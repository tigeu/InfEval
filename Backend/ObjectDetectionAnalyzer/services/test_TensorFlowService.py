from io import BytesIO
from unittest import TestCase
from unittest.mock import patch

from PIL import Image
from tensorflow import constant

from ObjectDetectionAnalyzer.services.TensorFlowService import TensorFlowService


class TestTensorFlowService(TestCase):
    """
    Test TensorFlowService
    """

    def setUp(self):
        self.tensor_flow_service = TensorFlowService()

    @patch('ObjectDetectionAnalyzer.services.TensorFlowService.TensorFlowService.get_detections')
    @patch('ObjectDetectionAnalyzer.services.TensorFlowService.TensorFlowService.load_model')
    def test_get_detections_for_images(self, load_model, get_detections):
        get_detections.return_value = [1, 2, 3]

        result = self.tensor_flow_service.get_detections_for_images("model_path", ["path1", "path2"])

        self.assertEqual(result['path1'], [1, 2, 3])
        self.assertEqual(result['path2'], [1, 2, 3])

    @patch('tensorflow.saved_model.load')
    def test_load_model_tf1(self, load):
        func = lambda x: x

        class SavedModel:
            def __init__(self):
                self.signatures = {'serving_default': func}

        saved_model = SavedModel()
        load.return_value = saved_model

        result = self.tensor_flow_service.load_model(True, "model_path")

        self.assertEqual(result, func)

    @patch('tensorflow.saved_model.load')
    def test_load_model_tf2(self, load):
        saved_model = lambda x: x
        load.return_value = saved_model

        result = self.tensor_flow_service.load_model(False, "model_path")

        self.assertEqual(result, saved_model)

    @patch('ObjectDetectionAnalyzer.services.TensorFlowService.TensorFlowService.extract_predictions')
    def test_get_detections(self, extract_predictions):
        predictions = [
            {'class': 1, 'confidence': 0.9, 'xmin': 50, 'ymin': 20, 'xmax': 60, 'ymax': 30}
        ]

        extract_predictions.return_value = predictions

        saved_model = lambda x: x

        file = BytesIO()
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save(file, 'png')

        result = self.tensor_flow_service.get_detections(saved_model, file)

        self.assertEqual(str(result[0]), str(predictions[0]))
        self.assertEqual(len(result), 1)

    def test_extract_predictions(self):
        classes = constant([1, 1, 2])
        scores = constant([0.9, 0.8, 0.5])
        boxes = constant([
            [0.2, 0.5, 0.3, 0.6],
            [0.3, 0.4, 0.3, 0.5],
            [0.6, 0.1, 1, 0.9]])

        image_width, image_height = (100, 100)

        predictions = [
            {'class': 1, 'confidence': 0.9, 'xmin': 50, 'ymin': 20, 'xmax': 60, 'ymax': 30},
            {'class': 2, 'confidence': 0.5, 'xmin': 10, 'ymin': 60, 'xmax': 90, 'ymax': 100}
        ]

        detections = {
            'detection_classes': [classes],
            'detection_scores': [scores],
            'detection_boxes': [boxes]
        }

        result = self.tensor_flow_service.extract_predictions(detections, image_width, image_height)

        self.assertEqual(str(result[0]), str(predictions[0]))
        self.assertEqual(str(result[1]), str(predictions[1]))
        self.assertEqual(len(result), 2)
