from pathlib import Path
from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.tasks.TasksModels import Tasks
from ObjectDetectionAnalyzer.tasks.TasksView import TasksView
from ObjectDetectionAnalyzer.upload.UploadModels import Models, Dataset


class TestTasksView(APITestCase):
    """
    Test TasksView
    """

    def setUp(self):
        self.url = reverse('tasks', kwargs={"task_name": "some_task"})
        self.parameters = {"task_description": "desc",
                           "file_name": "file_name",
                           "dataset_name": "dataset_name",
                           "model_name": "model_name"}

        self.tasks_view = TasksView()

        self.user = User.objects.create_user("test", "test@test.test", "test")

        self.client.force_authenticate(user=self.user)

    def test_task_view_without_dataset(self):
        response = self.client.post(self.url, data=self.parameters)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Dataset does not exist yet")

    def test_task_view_without_model(self):
        Dataset.objects.create(name="dataset_name", userId=self.user)

        response = self.client.post(self.url, data=self.parameters)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Model does not exist yet")

    def test_task_view_with_running_task(self):
        dataset = Dataset.objects.create(name="dataset_name", userId=self.user)
        model = Models.objects.create(name="model_name", userId=self.user)
        Tasks.objects.create(name="some_task", datasetId=dataset, modelId=model, userId=self.user)

        response = self.client.post(self.url, data=self.parameters)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "A task with this name is running already")

    @patch('ObjectDetectionAnalyzer.tasks.TasksView.TasksView.execute_task')
    def test_task_view(self, execute_task):
        dataset = Dataset.objects.create(name="dataset_name", userId=self.user)
        model = Models.objects.create(name="model_name", userId=self.user)

        response = self.client.post(self.url, data=self.parameters)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Task finished successfully")
        execute_task.assert_called_with(dataset, "desc", "file_name.csv", model, "some_task", self.user)

    @patch('ObjectDetectionAnalyzer.tasks.TasksView.TasksView.write_model_predictions')
    @patch('ObjectDetectionAnalyzer.tasks.TasksService.TasksService.replace_class_names')
    @patch('ObjectDetectionAnalyzer.services.JSONService.JSONService.read_label_map')
    @patch('ObjectDetectionAnalyzer.tasks.TasksView.TasksView.get_detections')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_image_files_from_dir')
    def test_execute_task(self, get_image_files_from_dir, get_detections, read_label_map, replace_class_names,
                          write_model_predictions):
        get_image_files_from_dir.return_value = ["image1.png", "image2.png"]
        get_detections.return_value = {"some_detections"}
        read_label_map.return_value = {"some_label_map"}

        dataset = Dataset.objects.create(name="dataset_name", userId=self.user)
        model = Models.objects.create(name="test_model", label_map_path="some_path", type="tf2", userId=self.user)

        self.tasks_view.execute_task(dataset, "desc", "file_name", model, "task_name", self.user)

        replace_class_names.assert_called_with({"some_detections"}, {"some_label_map"})
        write_model_predictions.assert_called_with(dataset, "file_name", {"some_detections"}, self.user)

    @patch('ObjectDetectionAnalyzer.tasks.TasksView.TasksView.write_model_predictions')
    @patch('ObjectDetectionAnalyzer.tasks.TasksView.TasksView.get_detections')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_image_files_from_dir')
    def test_execute_task_without_label_map(self, get_image_files_from_dir, get_detections, write_model_predictions):
        get_image_files_from_dir.return_value = ["image1.png", "image2.png"]
        get_detections.return_value = {"some_detections"}

        dataset = Dataset.objects.create(name="dataset_name", userId=self.user)
        model = Models.objects.create(name="test_model", type="tf2", userId=self.user)

        self.tasks_view.execute_task(dataset, "desc", "file_name", model, "task_name", self.user)

        write_model_predictions.assert_called_with(dataset, "file_name", {"some_detections"}, self.user)

    @patch('ObjectDetectionAnalyzer.upload.UploadModels.Predictions.objects.update_or_create')
    @patch('ObjectDetectionAnalyzer.services.CSVWriteService.CSVWriteService.write_predictions')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.create_dir')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_predictions_dir')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_dataset_dir')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_combined_dir')
    def test_write_model_predictions(self, get_combined_dir, get_dataset_dir, get_predictions_dir, create_dir,
                                     write_predictions, update_or_create):
        get_combined_dir.return_value = Path("data/user")
        get_dataset_dir.return_value = Path("data/user/dataset")
        get_predictions_dir.return_value = Path("data/user/dataset/predictions")
        file_path = Path("data/user/dataset/predictions/file_name")

        dataset = Dataset.objects.create(name="test_dataset", userId=self.user)

        self.tasks_view.write_model_predictions(dataset, "file_name", {"predictions"}, self.user)

        write_predictions.assert_called_with({"predictions"}, file_path)
        update_or_create.assert_called_with(name="file_name", path=file_path, datasetId=dataset, userId=self.user)

    @patch('ObjectDetectionAnalyzer.services.TensorFlowService.TensorFlowService.get_detections_for_task_images')
    def test_get_detections_tf1(self, get_detections_for_task_images):
        get_detections_for_task_images.return_value = {"image": [{"class": "some_class"}]}

        model = Models.objects.create(name="test_model", type="tf1", userId=self.user)
        result = self.tasks_view.get_detections(None, model, None)

        self.assertEqual(result, {"image": [{"class": "some_class"}]})
        get_detections_for_task_images.assert_called()

    @patch('ObjectDetectionAnalyzer.services.TensorFlowService.TensorFlowService.get_detections_for_task_images')
    def test_get_detections_tf2(self, get_detections_for_task_images):
        get_detections_for_task_images.return_value = {"image": [{"class": "some_class"}]}

        model = Models.objects.create(name="test_model", type="tf2", userId=self.user)
        result = self.tasks_view.get_detections(None, model, None)

        self.assertEqual(result, {"image": [{"class": "some_class"}]})
        get_detections_for_task_images.assert_called()

    @patch('ObjectDetectionAnalyzer.services.PyTorchService.PyTorchService.get_detections_for_task_images')
    def test_get_detections_pytorch(self, get_detections_for_task_images):
        get_detections_for_task_images.return_value = {"image": [{"class": "some_class"}]}

        model = Models.objects.create(name="test_model", type="pytorch", userId=self.user)
        result = self.tasks_view.get_detections(None, model, None)

        self.assertEqual(result, {"image": [{"class": "some_class"}]})
        get_detections_for_task_images.assert_called()

    @patch('ObjectDetectionAnalyzer.services.YoloService.YoloService.get_detections_for_task_images')
    def test_get_detections_yolov3(self, get_detections_for_task_images):
        get_detections_for_task_images.return_value = {"image": [{"class": "some_class"}]}

        model = Models.objects.create(name="test_model", type="yolov3", userId=self.user)
        result = self.tasks_view.get_detections(None, model, None)

        self.assertEqual(result, {"image": [{"class": "some_class"}]})
        get_detections_for_task_images.assert_called()

    @patch('ObjectDetectionAnalyzer.services.YoloService.YoloService.get_detections_for_task_images')
    def test_get_detections_yolov5(self, get_detections_for_task_images):
        get_detections_for_task_images.return_value = {"image": [{"class": "some_class"}]}

        model = Models.objects.create(name="test_model", type="yolov5", userId=self.user)
        result = self.tasks_view.get_detections(None, model, None)

        self.assertEqual(result, {"image": [{"class": "some_class"}]})
        get_detections_for_task_images.assert_called()
