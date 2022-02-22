from datetime import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.overview.OverviewView import OverviewView
from ObjectDetectionAnalyzer.tasks.TasksModels import Tasks
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions, Models


class TestOverviewView(APITestCase):
    """
    Test OverviewView
    """

    def setUp(self):
        self.url = reverse('overview')
        self.view = OverviewView()

        self.user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=self.user)

    @patch("ObjectDetectionAnalyzer.overview.OverviewView.OverviewView.get_tasks")
    @patch("ObjectDetectionAnalyzer.overview.OverviewView.OverviewView.get_models")
    @patch("ObjectDetectionAnalyzer.overview.OverviewView.OverviewView.get_predictions")
    @patch("ObjectDetectionAnalyzer.overview.OverviewView.OverviewView.get_datasets")
    def test_overview_view(self, get_datasets, get_predictions, get_models, get_tasks):
        get_datasets.return_value = {"some": "dataset"}
        get_predictions.return_value = {"some": "prediction"}
        get_models.return_value = {"some": "model"}
        get_tasks.return_value = {"some": "task"}

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["datasets"], {"some": "dataset"})
        self.assertEqual(response.data["predictions"], {"some": "prediction"})
        self.assertEqual(response.data["models"], {"some": "model"})
        self.assertEqual(response.data["tasks"], {"some": "task"})

    def test_get_datasets(self):
        date = datetime(2022, 2, 22, 22, 22, 22)
        date_str = "2022-02-22 22:22:22"
        dataset1 = Dataset.objects.create(name="dataset1", ground_truth_path="path", userId=self.user, uploaded_at=date)
        Dataset.objects.create(name="dataset2", ground_truth_path="", userId=self.user, uploaded_at=date)

        Predictions.objects.create(name="pred1", datasetId=dataset1, userId=self.user)

        datasets = self.view.get_datasets(self.user)

        self.assertEqual(datasets, [
            {"name": "dataset1", "groundTruth": True, "predictions": True, "uploaded": date_str},
            {"name": "dataset2", "groundTruth": False, "predictions": False, "uploaded": date_str}
        ])

    def test_get_predictions(self):
        date = datetime(2022, 2, 22, 22, 22, 22)
        date_str = "2022-02-22 22:22:22"
        dataset1 = Dataset.objects.create(name="dataset1", ground_truth_path="path", userId=self.user, uploaded_at=date)

        Predictions.objects.create(name="pred1", datasetId=dataset1, userId=self.user, uploaded_at=date)
        Predictions.objects.create(name="pred2", datasetId=dataset1, userId=self.user, uploaded_at=date)

        predictions = self.view.get_predictions(self.user)

        self.assertEqual(predictions, [
            {"name": "pred1", "dataset": "dataset1", "uploaded": date_str},
            {"name": "pred2", "dataset": "dataset1", "uploaded": date_str}
        ])

    def test_get_models(self):
        date = datetime(2022, 2, 22, 22, 22, 22)
        date_str = "2022-02-22 22:22:22"

        Models.objects.create(name="model1", type="tf2", label_map_path="path", userId=self.user, uploaded_at=date_str)
        Models.objects.create(name="model2", type="pytorch", label_map_path="", userId=self.user, uploaded_at=date_str)

        models = self.view.get_models(self.user)

        self.assertEqual(models, [
            {"name": "model1", "type": "TensorFlow 2", "labelMap": True, "uploaded": date_str},
            {"name": "model2", "type": "PyTorch", "labelMap": False, "uploaded": date_str}
        ])

    def test_get_tasks(self):
        date = datetime(2022, 2, 22, 22, 22, 22)
        date_str = "2022-02-22 22:22:22"

        dataset1 = Dataset.objects.create(name="dataset1", ground_truth_path="path", userId=self.user, uploaded_at=date)
        model1 = Models.objects.create(name="model1", type="tf2", label_map_path="path", userId=self.user,
                                       uploaded_at=date_str)

        Tasks.objects.create(name="task1", description="desc1", progress=50, file_name="file1", started=date,
                             datasetId=dataset1, modelId=model1, userId=self.user)
        Tasks.objects.create(name="task2", description="desc2", progress=100, file_name="file2", started=date,
                             finished=date, datasetId=dataset1, modelId=model1, userId=self.user)

        tasks = self.view.get_tasks(self.user)

        self.assertEqual(tasks, [
            {"name": "task1", "description": "desc1", "progress": 50, "fileName": "file1",
             "started": date_str, "finished": "", "dataset": "dataset1", "model": "model1"},
            {"name": "task2", "description": "desc2", "progress": 100, "fileName": "file2",
             "started": date_str, "finished": date_str, "dataset": "dataset1", "model": "model1"}
        ])
