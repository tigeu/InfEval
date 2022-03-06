from django.db import models
from django.utils import timezone
from rest_framework.authtoken.admin import User

from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Models


class Tasks(models.Model):
    """
    Model for Tasks
    """

    class Meta:
        unique_together = ("name", "userId")

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    file_name = models.CharField(max_length=50)
    progress = models.FloatField(default=0)
    started = models.DateTimeField(default=timezone.now)
    finished = models.DateTimeField(null=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    datasetId = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    modelId = models.ForeignKey(Models, on_delete=models.CASCADE)
