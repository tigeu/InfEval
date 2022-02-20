from enum import Enum


class ModelTypes(Enum):
    def __str__(self):
        if self.value == 'pytorch':
            return 'PyTorch'
        elif self.value == 'tf1':
            return 'TensorFlow 1'
        elif self.value == 'tf2':
            return 'TensorFlow 2'
        elif self.value == 'yolov3':
            return 'YOLOv3'
        elif self.value == 'yolov5':
            return 'YOLOv5'

    PYTORCH = 'pytorch'
    TENSORFLOW1 = 'tf1'
    TENSORFLOW2 = 'tf2'
    YOLOV3 = 'yolov3'
    YOLOV5 = 'yolov5'
