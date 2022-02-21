from unittest import TestCase

from ObjectDetectionAnalyzer.upload.ModelTypes import ModelTypes


class TestModelTypes(TestCase):
    """
    Test ModelTypes
    """

    def test_model_type_pytorch(self):
        result = str(ModelTypes.PYTORCH)

        self.assertEqual(result, "PyTorch")

    def test_model_type_tf1(self):
        result = str(ModelTypes.TENSORFLOW1)

        self.assertEqual(result, "TensorFlow 1")

    def test_model_type_tf2(self):
        result = str(ModelTypes.TENSORFLOW2)

        self.assertEqual(result, "TensorFlow 2")

    def test_model_type_yolov3(self):
        result = str(ModelTypes.YOLOV3)

        self.assertEqual(result, "YOLOv3")

    def test_model_type_yolov5(self):
        result = str(ModelTypes.YOLOV5)

        self.assertEqual(result, "YOLOv5")
       