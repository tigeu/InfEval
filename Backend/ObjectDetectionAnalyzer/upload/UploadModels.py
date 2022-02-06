from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from ObjectDetectionAnalyzer.upload.ModelTypes import ModelTypes


class Dataset(models.Model):
    class Meta:
        unique_together = ("name", "userId")

    name = models.CharField(max_length=50)
    path = models.FilePathField()
    ground_truth_path = models.FilePathField(blank=True)
    label_map_path = models.FilePathField(blank=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)


class Predictions(models.Model):
    class Meta:
        unique_together = ("name", "datasetId", "userId")

    name = models.CharField(max_length=50)
    path = models.FilePathField()
    datasetId = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)


class Models(models.Model):
    class Meta:
        unique_together = ("name", "type", "userId")

    MODEL_TYPES = (
        (ModelTypes.PYTORCH, 'PyTorch'),
        (ModelTypes.TENSORFLOW1, 'TensorFlow 1'),
        (ModelTypes.TENSORFLOW2, 'TensorFlow 2'),
        (ModelTypes.YOLOV3, 'Yolo v3'),
        (ModelTypes.YOLOV5, 'Yolo v5'),
    )

    name = models.CharField(max_length=50, unique=True)
    path = models.FilePathField()
    type = models.CharField(choices=MODEL_TYPES, max_length=7)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)
