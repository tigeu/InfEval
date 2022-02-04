from pathlib import Path
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.upload.UploadModels import Dataset
from ObjectDetectionAnalyzer.upload.views.UploadLabelMapView import UploadLabelMapView


class TestUploadLabelMapView(APITestCase):
    """
    Test UploadLabelMapView
    """

    def setUp(self):
        self.view = UploadLabelMapView()
        self.user_dir = Path("dir/test")

    def test_requires_dataset(self):
        result = self.view.requires_dataset()
        self.assertEqual(result, True)

    @patch('ObjectDetectionAnalyzer.upload.UploadService.UploadService.is_label_map_valid')
    def test_is_file_valid(self, is_label_map_valid):
        is_label_map_valid.return_value = True
        result = self.view.is_file_valid(Path("tmp_file_path"))
        self.assertEqual(result, True)

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_dataset_dir')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_combined_dir')
    def test_get_target_dir(self, get_combined_dir, get_dataset_dir):
        get_combined_dir.return_value = Path("data/test")
        get_dataset_dir.return_value = Path("data/test/datasets/test_dataset")

        result = self.view.get_target_dir("test", "test_dataset")

        self.assertEqual(result, Path("data/test/datasets/test_dataset"))

    @patch('django.db.models.query.QuerySet.update')
    @patch('ObjectDetectionAnalyzer.upload.UploadService.UploadService.save_data')
    def test_save_data_with_dataset(self, save_data, update):
        user = User.objects.create_user("test", "test@test.test", "test")
        Dataset.objects.create(name="test_dataset", path=Path("target"), userId=user)
        dataset = Dataset.objects.filter(name="test_dataset", userId=user)

        self.view.save_data(Path("tmp"), Path("target"), "test_dataset", None, dataset, user, "label_map")

        save_data.assert_called_with(Path("tmp"), Path("target"), 'label_map.txt')
        update.assert_called()
