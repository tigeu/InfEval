import io
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.upload.UploadModels import Dataset
from ObjectDetectionAnalyzer.upload.views.UploadBaseView import UploadBaseView


class TestUploadBaseView(APITestCase):
    """
    Test UploadBaseView
    Dataset url is used for testing, applies to others as well as specific methods are being
    mocked anyway.
    """

    def setUp(self):
        self.url = reverse('upload-dataset', kwargs={'file_name': 'test_dataset.zip'})
        self.request = {
            "file": io.StringIO(),
            "dataset_name": "test_dataset",
            "model_name": "model_name"
        }
        self.user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=self.user)

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.delete_tmp_file')
    @patch('ObjectDetectionAnalyzer.upload.views.UploadDatasetView.UploadDatasetView.save_data')
    @patch('ObjectDetectionAnalyzer.upload.views.UploadDatasetView.UploadDatasetView.create_dir')
    @patch('ObjectDetectionAnalyzer.upload.views.UploadDatasetView.UploadDatasetView.get_target_dir')
    @patch('ObjectDetectionAnalyzer.upload.views.UploadDatasetView.UploadDatasetView.is_file_valid')
    @patch('ObjectDetectionAnalyzer.upload.views.UploadDatasetView.UploadDatasetView.requires_dataset')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.save_tmp_file')
    def test_upload_base_view(self, save_tmp_file, requires_dataset, is_file_valid, get_target_dir, create_dir,
                              save_data, delete_tmp_file):
        save_tmp_file.return_value = Path("tmp_path")
        requires_dataset.return_value = True
        is_file_valid.return_value = True
        get_target_dir.return_value = Path("target")
        create_dir.return_value = True

        Dataset.objects.create(name="test_dataset", path=Path("target"), userId=self.user)

        response = self.client.put(self.url, self.request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.save_tmp_file')
    def test_upload_base_view_without_tmp_file(self, save_tmp_file):
        save_tmp_file.return_value = None

        response = self.client.put(self.url, self.request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "File could not be saved")

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.delete_tmp_file')
    @patch('ObjectDetectionAnalyzer.upload.views.UploadDatasetView.UploadDatasetView.requires_dataset')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.save_tmp_file')
    def test_upload_base_view_without_required_dataset(self, save_tmp_file, requires_dataset, delete_tmp_file):
        save_tmp_file.return_value = Path("tmp_path")
        requires_dataset.return_value = True

        response = self.client.put(self.url, self.request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Dataset does not exist yet")

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.delete_tmp_file')
    @patch('ObjectDetectionAnalyzer.upload.views.UploadDatasetView.UploadDatasetView.is_file_valid')
    @patch('ObjectDetectionAnalyzer.upload.views.UploadDatasetView.UploadDatasetView.requires_dataset')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.save_tmp_file')
    def test_upload_base_view_with_invalid_file(self, save_tmp_file, requires_dataset, is_file_valid, delete_tmp_file):
        save_tmp_file.return_value = Path("tmp_path")
        requires_dataset.return_value = True
        is_file_valid.return_value = False

        Dataset.objects.create(name="test_dataset", path=Path("target"), userId=self.user)

        response = self.client.put(self.url, self.request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Invalid file uploaded")

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.delete_tmp_file')
    @patch('ObjectDetectionAnalyzer.upload.views.UploadDatasetView.UploadDatasetView.create_dir')
    @patch('ObjectDetectionAnalyzer.upload.views.UploadDatasetView.UploadDatasetView.get_target_dir')
    @patch('ObjectDetectionAnalyzer.upload.views.UploadDatasetView.UploadDatasetView.is_file_valid')
    @patch('ObjectDetectionAnalyzer.upload.views.UploadDatasetView.UploadDatasetView.requires_dataset')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.save_tmp_file')
    def test_upload_base_view_without_create_dir(self, save_tmp_file, requires_dataset, is_file_valid, get_target_dir,
                                                 create_dir, delete_tmp_file):
        save_tmp_file.return_value = Path("tmp_path")
        requires_dataset.return_value = True
        is_file_valid.return_value = True
        get_target_dir.return_value = Path("target")
        create_dir.return_value = False

        Dataset.objects.create(name="test_dataset", path=Path("target"), userId=self.user)

        response = self.client.put(self.url, self.request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Dataset directory could not be created")

    def test_dummy_method_is_file_valid(self):
        view = UploadBaseView()
        result = view.is_file_valid(Path("tmp_file_Path"))
        self.assertEqual(result, None)

    def test_dummy_method_get_target_dir(self):
        view = UploadBaseView()
        result = view.get_target_dir("test", "test_dataset", "test_model")
        self.assertEqual(result, None)

    def test_dummy_method_save_data(self):
        view = UploadBaseView()
        result = view.save_data(Path("tmp"), Path("target"), "test_dataset", None, None, None, self.user, "file_name")
        self.assertEqual(result, None)

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.create_dir')
    def test_create_dir(self, create_dir):
        create_dir.return_value = True
        view = UploadBaseView()
        result = view.create_dir(Path("dir"))

        create_dir.expect_called_with(Path("dir"), False)
