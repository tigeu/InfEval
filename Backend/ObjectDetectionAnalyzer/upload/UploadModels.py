from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Dataset(models.Model):
    name = models.CharField(max_length=50, unique=True)
    path = models.FilePathField()
    ground_truth_path = models.FilePathField(blank=True)
    label_map_path = models.FilePathField(blank=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)


class Predictions(models.Model):
    name = models.CharField(max_length=50, unique=True)
    path = models.FilePathField()
    datasetId = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)


class Models(models.Model):
    name = models.CharField(max_length=50, unique=True)
    path = models.FilePathField()
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)
