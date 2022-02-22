from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.tasks.TasksModels import Tasks
from ObjectDetectionAnalyzer.upload.UploadModels import Models, Dataset


class TestTasksListView(APITestCase):
    """
    Test TasksListView
    """

    def setUp(self):
        self.url = reverse('tasks-list')
        self.delete_url = reverse('tasks-list', kwargs={'task': 'task_name'})
        self.user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=self.user)
        self.dataset = Dataset.objects.create(name="dataset", userId=self.user)
        self.model = Models.objects.create(name="model", type="tf2", userId=self.user)

    def test_tasks_list(self):
        now = timezone.now()
        now_task2 = now + timedelta(days=1)
        now_task3 = now_task2 + timedelta(days=1)
        self.task1 = Tasks.objects.create(name="task1", file_name="file1", progress=0, started=now,
                                          datasetId=self.dataset, modelId=self.model, userId=self.user)
        self.task2 = Tasks.objects.create(name="task2", file_name="file2", progress=50, started=now_task2,
                                          datasetId=self.dataset, modelId=self.model, userId=self.user)
        self.task3 = Tasks.objects.create(name="task3", file_name="file3", progress=100, started=now_task3,
                                          finished=now, datasetId=self.dataset, modelId=self.model, userId=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # only compare most important properties
        self.assertEqual(response.data[0]['name'], 'task3')
        self.assertEqual(response.data[0]['dataset'], 'dataset')
        self.assertEqual(response.data[0]['model'], 'model')
        self.assertEqual(response.data[0]['finished'], now.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response.data[1]['name'], 'task2')
        self.assertEqual(response.data[1]['dataset'], 'dataset')
        self.assertEqual(response.data[1]['model'], 'model')
        self.assertEqual(response.data[1]['finished'], None)
        self.assertEqual(response.data[2]['name'], 'task1')
        self.assertEqual(response.data[2]['dataset'], 'dataset')
        self.assertEqual(response.data[2]['model'], 'model')
        self.assertEqual(response.data[2]['finished'], None)

    def test_dataset_list_with_without_data(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    @patch('ObjectDetectionAnalyzer.tasks.TasksModels.Tasks.delete')
    def test_delete(self, delete):
        Tasks.objects.create(name="task_name", file_name="file1", progress=0,
                             datasetId=self.dataset, modelId=self.model, userId=self.user)

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Successfully deleted task")
        delete.assert_called()
