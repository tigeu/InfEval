from enum import Enum


class ModelTypes(Enum):
    def __str__(self):
        return self.value[0]

    PYTORCH = 'pytorch',
    TENSORFLOW1 = 'tf1',
    TENSORFLOW2 = 'tf2',
    YOLOV3 = 'yolov3',
    YOLOV5 = 'yolov5',
