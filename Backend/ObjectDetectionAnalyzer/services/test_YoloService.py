from io import BytesIO
from unittest import TestCase
from unittest.mock import patch

import pandas as pd
from PIL import Image

from ObjectDetectionAnalyzer.services.YoloService import YoloService


class TestYoloService(TestCase):
    """
    Test YoloService
    """

    def setUp(self):
        self.yolo_service = YoloService()

    def test_yolo_v5(self):
        model_path = "/home/leon/Development/ObjectDetectionAnalyzer/Backend/YOLO/yolov5"
        weight_path = "/home/leon/Development/Python/JupyterLab/yolov5/yolov5x6.pt"
        # image_paths = ["/home/leon/Development/Python/JupyterLab/2018_0714_112546_051.JPG"]
        file = BytesIO()
        file.name = "test_image"
        image = Image.new('RGBA', size=(500, 500))
        image.save(file, 'png')
        image = Image.open(file)

        image_paths = [image]
        predictions = self.yolo_service.get_detections_for_images(model_path, weight_path, image_paths)
        for image_path, preds in predictions.items():
            print(image_path)
            for pred in preds:
                print(pred)

    @patch('ObjectDetectionAnalyzer.services.YoloService.YoloService.extract_predictions')
    @patch("torch.hub.load")
    def test_get_detections_for_images(self, load, extract_predictions):
        load.return_value = lambda x: x
        extract_predictions.return_value = [1, 2, 3]

        result = self.yolo_service.get_detections_for_images("yolo_dir", "weight_path", ["path1", "path2"])

        self.assertEqual(result['path1'], [1, 2, 3])
        self.assertEqual(result['path2'], [1, 2, 3])

    def test_extract_predictions(self):
        class Det:
            def __init__(self):
                self.name = [1, 1, 2]
                self.confidence = [0.9, 0.8, 0.5]
                self.xmin = [50, 50, 10]
                self.ymin = [20, 30, 60]
                self.xmax = [60, 50, 90]
                self.ymax = [30, 30, 100]

        df = pd.DataFrame(
            {"xyxy": [Det()]}
        )

        class Result:
            def pandas(self):
                return df

        predictions = [
            {'class': 1, 'confidence': 0.9, 'xmin': 50, 'ymin': 20, 'xmax': 60, 'ymax': 30},
            {'class': 2, 'confidence': 0.5, 'xmin': 10, 'ymin': 60, 'xmax': 90, 'ymax': 100}
        ]

        result = self.yolo_service.extract_predictions(Result())

        self.assertEqual(str(result[0]), str(predictions[0]))
        self.assertEqual(str(result[1]), str(predictions[1]))
        self.assertEqual(len(result), 2)
