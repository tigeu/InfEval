from pathlib import Path
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.upload.UploadModels import Models
from ObjectDetectionAnalyzer.upload.views.UploadModelView import UploadModelView


class TestUploadModelView(APITestCase):
    """
    Test UploadModelView
    """

    def setUp(self):
        self.view = UploadModelView()
        self.user_dir = Path("dir/test")

    def test_requires_dataset(self):
        result = self.view.requires_dataset()
        self.assertEqual(result, False)

    @patch('ObjectDetectionAnalyzer.upload.UploadService.UploadService.is_model_valid')
    def test_is_file_valid(self, is_prediction_valid):
        is_prediction_valid.return_value = True
        result = self.view.is_file_valid(Path("tmp_file_path"))
        self.assertEqual(result, True)

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_model_dir')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_combined_dir')
    def test_get_target_dir(self, get_combined_dir, get_model_dir):
        get_combined_dir.return_value = Path("data/test")
        get_model_dir.return_value = Path("data/test/models")

        result = self.view.get_target_dir("test", "test_dataset")

        self.assertEqual(result, Path("data/test/models"))

    @patch('django.db.models.query.QuerySet.update')
    @patch('ObjectDetectionAnalyzer.upload.UploadService.UploadService.save_data')
    def test_save_data_with_prediction(self, save_data, update):
        save_data.return_value = Path("target")
        user = User.objects.create_user("test", "test@test.test", "test")

        Models.objects.create(name="model", path="target", userId=user)

        self.view.save_data(Path("tmp"), Path("target"), None, None, user, "model")

        save_data.assert_called_with(Path("tmp"), Path("target"), "model")
        update.assert_called()

    @patch('django.db.models.query.QuerySet.create')
    @patch('ObjectDetectionAnalyzer.upload.UploadService.UploadService.save_data')
    def test_save_data_without_prediction(self, save_data, create):
        save_data.return_value = Path("target")
        user = User.objects.create_user("test", "test@test.test", "test")

        self.view.save_data(Path("tmp"), Path("target"), None, None, user, "model")

        save_data.assert_called_with(Path("tmp"), Path("target"), "model")
        create.assert_called_with(name="model", path=Path("target"), userId=user)
