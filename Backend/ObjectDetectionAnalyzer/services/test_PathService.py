import io
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, mock_open

from ObjectDetectionAnalyzer.services.PathService import PathService


class TestPathService(TestCase):
    """
    Test PathService
    """

    def setUp(self):
        self.path_service = PathService()
        self.directory = Path("dir")
        self.user_name = "user"

    def test_path_service_get_combined_dir(self):
        user_dir = self.path_service.get_combined_dir(self.directory, self.user_name)

        self.assertEqual(user_dir, Path("dir/user"))

    def test_path_service_get_combined_dir_without_user_name(self):
        user_dir = self.path_service.get_combined_dir(self.directory, "")

        self.assertEqual(user_dir, None)

    def test_path_service_get_combined_dir_without_directory(self):
        user_dir = self.path_service.get_combined_dir("", self.user_name)

        self.assertEqual(user_dir, None)

    @patch('pathlib.Path.mkdir')
    def test_create_dir(self, mkdir):
        result = self.path_service.create_dir(Path(self.directory))
        self.assertEqual(result, True)

    def test_create_dir_without_dir(self):
        result = self.path_service.create_dir(None)
        self.assertEqual(result, False)

    @patch('pathlib.Path.mkdir')
    @patch('pathlib.Path.is_dir')
    @patch('shutil.rmtree')
    def test_create_dir_with_recreate(self, rmtree, is_dir, mkdir):
        is_dir.return_value = True
        result = self.path_service.create_dir(Path("dir"), True)
        self.assertEqual(result, True)
        rmtree.assert_called_with(Path("dir"))

    def test_get_dataset_dir(self):
        result = self.path_service.get_dataset_dir(Path("user_dir"), "test_dataset")
        self.assertEqual(result, Path("user_dir/datasets/test_dataset"))

    def test_get_dataset_dir_without_user_dir(self):
        result = self.path_service.get_dataset_dir(None, "test_dataset")
        self.assertEqual(result, None)

    def test_get_dataset_dir_without_name(self):
        result = self.path_service.get_dataset_dir(Path("user_dir"), "")
        self.assertEqual(result, None)

    def test_get_prediction_dir(self):
        result = self.path_service.get_predictions_dir(Path("dataset_dir"))
        self.assertEqual(result, Path("dataset_dir/predictions"))

    def test_get_prediction_dir_without_dataset_dir(self):
        result = self.path_service.get_predictions_dir(None)
        self.assertEqual(result, None)

    def test_get_model_dir(self):
        result = self.path_service.get_model_dir(Path("user_dir"))
        self.assertEqual(result, Path("user_dir/models"))

    def test_get_model_dir_without_user_dir(self):
        result = self.path_service.get_model_dir(None)
        self.assertEqual(result, None)

    @patch('builtins.open')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_combined_dir')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.create_dir')
    def test_save_tmp_file(self, create_dir, get_combined_dir, open):
        create_dir.return_value = True
        get_combined_dir.return_value = "tmp_dir/file_name"
        open = mock_open()
        file = io.StringIO("some data")

        result = self.path_service.save_tmp_file("tmp_dir", "file_name", file)

        self.assertEqual(result, "tmp_dir/file_name")

    @patch('builtins.open')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_combined_dir')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.create_dir')
    def test_save_tmp_file_without_tmp_dir(self, create_dir, get_combined_dir, open):
        create_dir.return_value = False
        result = self.path_service.save_tmp_file(None, "file_name", None)

        self.assertEqual(result, None)

    @patch('pathlib.Path.unlink')
    def test_delete_tmp_file(self, unlink):
        self.path_service.delete_tmp_file("tmp_file_path")
        unlink.assert_called_with("tmp_file_path")
