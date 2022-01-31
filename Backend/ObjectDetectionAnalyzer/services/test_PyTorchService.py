from io import BytesIO
from unittest import TestCase
from unittest.mock import patch

import torch
from PIL import Image
from torchvision.transforms import transforms

from ObjectDetectionAnalyzer.services.PyTorchService import PyTorchService


class TestPyTorchService(TestCase):
    """
    Test PyTorchService
    """

    def setUp(self):
        self.pytorch_service = PyTorchService()

    @patch('ObjectDetectionAnalyzer.services.PyTorchService.PyTorchService.get_detections')
    @patch('ObjectDetectionAnalyzer.services.PyTorchService.PyTorchService.load_model')
    def test_get_detections_for_images(self, load_model, get_detections):
        get_detections.return_value = [1, 2, 3]
        load_model.return_value = lambda x: x

        result = self.pytorch_service.get_detections_for_images("model_path", ["path1", "path2"])

        self.assertEqual(result['path1'], [1, 2, 3])
        self.assertEqual(result['path2'], [1, 2, 3])

    @patch("torch.load")
    def test_load_model(self, load):
        class Model:
            def eval(self):
                return self

            def to(self, device):
                return self

        model = Model()
        load.return_value = model

        result = self.pytorch_service.load_model("model_path", "device")

        self.assertEqual(result, model)

    @patch('ObjectDetectionAnalyzer.services.PyTorchService.PyTorchService.extract_predictions')
    def test_get_detections(self, extract_predictions):
        predictions = [
            {'class': 1, 'confidence': 0.9, 'xmin': 50, 'ymin': 20, 'xmax': 60, 'ymax': 30}
        ]

        extract_predictions.return_value = predictions

        file = BytesIO()
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save(file, 'png')

        model = lambda x: x
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        transform = transforms.Compose([
            transforms.ToTensor(),
        ])

        result = self.pytorch_service.get_detections(model, device, file, transform)

        self.assertEqual(str(result[0]), str(predictions[0]))
        self.assertEqual(len(result), 1)

    def test_extract_predictions(self):
        labels = torch.tensor([1, 1, 2])
        scores = torch.tensor([0.9, 0.8, 0.5])
        boxes = torch.tensor([
            [50, 20, 60, 30],
            [40, 30, 50, 30],
            [10, 60, 90, 100]], dtype=torch.float64)

        outputs = [{
            'labels': labels,
            'scores': scores,
            'boxes': boxes
        }]

        predictions = [
            {'class': 1, 'confidence': 0.9, 'xmin': 50, 'ymin': 20, 'xmax': 60, 'ymax': 30},
            {'class': 2, 'confidence': 0.5, 'xmin': 10, 'ymin': 60, 'xmax': 90, 'ymax': 100}
        ]

        result = self.pytorch_service.extract_predictions(outputs)

        self.assertEqual(str(result[0]), str(predictions[0]))
        self.assertEqual(str(result[1]), str(predictions[1]))
        self.assertEqual(len(result), 2)
