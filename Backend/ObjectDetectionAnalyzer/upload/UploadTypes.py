from enum import Enum


class UploadTypes(Enum):
    """
    Enum describing what kind of data was uploaded
    """
    DATASET = 0
    GROUND_TRUTH = 1
    LABEL_MAP = 2
    PREDICTIONS = 3
    TF_MODEL = 4
