from pathlib import Path
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.upload.UploadModels import Predictions, Dataset
from ObjectDetectionAnalyzer.upload.views.UploadPredictionsView import UploadPredictionsView


class TestUploadPredictionsView(APITestCase):
    """
    Test UploadPredictionsView
    """

    def setUp(self):
        self.view = UploadPredictionsView()
        self.user_dir = Path("dir/test")

    def test_requires_dataset(self):
        result = self.view.requires_dataset()
        self.assertEqual(result, True)

    @patch('ObjectDetectionAnalyzer.upload.UploadService.UploadService.is_prediction_valid')
    def test_is_file_valid(self, is_prediction_valid):
        is_prediction_valid.return_value = True
        result = self.view.is_file_valid(Path("tmp_file_path"))
        self.assertEqual(result, True)

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_predictions_dir')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_dataset_dir')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_combined_dir')
    def test_get_target_dir(self, get_combined_dir, get_dataset_dir, get_predictions_dir):
        get_combined_dir.return_value = Path("data/test")
        get_dataset_dir.return_value = Path("data/test/datasets/test_dataset")
        get_predictions_dir.return_value = Path("data/test/datasets/test_dataset/predictions")

        result = self.view.get_target_dir("test", "test_dataset")

        self.assertEqual(result, Path("data/test/datasets/test_dataset/predictions"))

    @patch('django.db.models.query.QuerySet.update')
    @patch('ObjectDetectionAnalyzer.upload.UploadService.UploadService.save_data')
    def test_save_data_with_prediction(self, save_data, update):
        user = User.objects.create_user("test", "test@test.test", "test")
        dataset = Dataset.objects.create(name="test_dataset", path=Path("target"), userId=user)

        Predictions.objects.create(name="pred", path="target", datasetId=dataset, userId=user)

        self.view.save_data(Path("tmp"), Path("target"), "test_dataset", None, user, "pred")

        save_data.assert_called_with(Path("tmp"), Path("target"), "pred")
        update.assert_called()

    @patch('django.db.models.query.QuerySet.create')
    @patch('ObjectDetectionAnalyzer.upload.UploadService.UploadService.save_data')
    def test_save_data_without_prediction(self, save_data, create):
        save_data.return_value = Path("target")
        user = User.objects.create_user("test", "test@test.test", "test")
        Dataset.objects.create(name="test_dataset", path=Path("target"), userId=user)
        dataset = Dataset.objects.filter(name="test_dataset", userId=user)

        self.view.save_data(Path("tmp"), Path("target"), "test_dataset", dataset, user, "pred")

        save_data.assert_called_with(Path("tmp"), Path("target"), "pred")
        create.assert_called_with(name="pred", path=Path("target"), datasetId=dataset.first(), userId=user)
