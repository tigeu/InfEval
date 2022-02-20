from pathlib import Path
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.upload.UploadModels import Models
from ObjectDetectionAnalyzer.upload.views.UploadYolov3ModelView import UploadYolov3ModelView


class TestUploadYolov3ModelView(APITestCase):
    """
    Test UploadYolov3ModelView
    """

    def setUp(self):
        self.view = UploadYolov3ModelView()
        self.user_dir = Path("dir/test")

    def test_requires_dataset(self):
        result = self.view.requires_dataset()
        self.assertEqual(result, False)

    @patch('ObjectDetectionAnalyzer.upload.UploadService.UploadService.is_yolo_valid')
    def test_is_file_valid(self, is_yolo_valid):
        is_yolo_valid.return_value = True
        result = self.view.is_file_valid(Path("tmp_file_path"))
        self.assertEqual(result, True)

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_model_dir')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_combined_dir')
    def test_get_target_dir(self, get_combined_dir, get_model_dir):
        get_combined_dir.return_value = Path("data/test")
        get_model_dir.return_value = Path("data/test/models/test_model")

        result = self.view.get_target_dir("test", "", "test_model")

        self.assertEqual(result, Path("data/test/models/test_model"))

    @patch('django.db.models.query.QuerySet.update')
    @patch('ObjectDetectionAnalyzer.upload.UploadService.UploadService.save_data')
    def test_save_data_with_prediction(self, save_data, update):
        save_data.return_value = Path("target")
        user = User.objects.create_user("test", "test@test.test", "test")

        Models.objects.create(name="model_name", path="target", type='yolov3', userId=user)

        self.view.save_data(Path("tmp"), Path("target"), None, "model_name", None, None, user, "model")

        save_data.assert_called_with(Path("tmp"), Path("target"), "model")
        update.assert_called()

    @patch('django.db.models.query.QuerySet.create')
    @patch('ObjectDetectionAnalyzer.upload.UploadService.UploadService.save_data')
    def test_save_data_without_prediction(self, save_data, create):
        save_data.return_value = Path("new_model_name/new_model_name")
        user = User.objects.create_user("test", "test@test.test", "test")

        self.view.save_data(Path("tmp"), Path("new_model_name"), None, "new_model_name", None, None, user, "model")

        save_data.assert_called_with(Path("tmp"), Path("new_model_name"), "model")
        create.assert_called_with(name="new_model_name",
                                  path=Path("new_model_name/new_model_name"), type='yolov3', userId=user)
