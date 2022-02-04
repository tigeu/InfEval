import io
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from ObjectDetectionAnalyzer.upload.UploadService import UploadService


class TestUploadService(TestCase):
    """
    Test UploadService
    """

    def setUp(self):
        self.upload_service = UploadService()
        self.files = ["test.csv", "test2.jpg", "test3.png", "test4.c", "test5", "test6.zip"]

    @patch("zipfile.ZipFile")
    @patch("zipfile.is_zipfile")
    def test_is_zip_valid_with_images(self, is_zipfile, ZipFile):
        is_zipfile.return_value = True
        ZipFile.return_value.__enter__.return_value.namelist.return_value = self.files
        image_endings = {".jpg", ".png"}

        result = self.upload_service.is_zip_valid(ZipFile, image_endings)

        self.assertEqual(result, True)

    @patch("zipfile.ZipFile")
    @patch("zipfile.is_zipfile")
    def test_is_zip_valid_without_images(self, is_zipfile, ZipFile):
        is_zipfile.return_value = True
        ZipFile.return_value.__enter__.return_value.namelist.return_value = ["test.csv", "test4.c"]
        image_endings = {".jpg", ".png"}

        result = self.upload_service.is_zip_valid(ZipFile, image_endings)

        self.assertEqual(result, False)

    def test_is_zip_valid_with_bad_zip(self):
        image_endings = {".jpg", ".png"}
        zip = io.BytesIO("test".encode())

        result = self.upload_service.is_zip_valid(zip, image_endings)

        self.assertEqual(result, False)

    @patch('ObjectDetectionAnalyzer.upload.validators.GroundTruthValidator.GroundTruthValidator.is_valid')
    def test_is_ground_truth_valid(self, is_valid):
        is_valid.return_value = True
        result = self.upload_service.is_ground_truth_valid("tmp")

        self.assertEqual(result, True)
        is_valid.assert_called()

    @patch('ObjectDetectionAnalyzer.upload.validators.LabelMapValidator.LabelMapValidator.is_valid')
    def test_is_label_map_valid(self, is_valid):
        is_valid.return_value = True
        result = self.upload_service.is_label_map_valid("tmp")

        self.assertEqual(result, True)
        is_valid.assert_called()

    @patch('ObjectDetectionAnalyzer.upload.validators.PredictionsValidator.PredictionsValidator.is_valid')
    def test_is_prediction_valid(self, is_valid):
        is_valid.return_value = True
        result = self.upload_service.is_prediction_valid("tmp")

        self.assertEqual(result, True)
        is_valid.assert_called()

    @patch('ObjectDetectionAnalyzer.upload.validators.ModelValidator.ModelValidator.is_pytorch_valid')
    def test_is_pytorch_model_valid(self, is_valid):
        is_valid.return_value = True
        result = self.upload_service.is_pytorch_valid("tmp")

        self.assertEqual(result, True)
        is_valid.assert_called()

    @patch('shutil.copyfileobj')
    @patch("builtins.open")
    @patch("zipfile.ZipFile")
    @patch("zipfile.is_zipfile")
    def test_save_compressed_data(self, is_zipfile, ZipFile, open, copyfileobj):
        is_zipfile.return_value = True
        ZipFile.return_value.__enter__.return_value.namelist.return_value = self.files

        image_endings = {".jpg", ".png"}

        self.upload_service.save_compressed_data("tmp", "test_dataset", image_endings)

        self.assertEqual(copyfileobj.call_count, 2)

    @patch("shutil.copy")
    def test_save_data(self, copy):
        result = self.upload_service.save_data("tmp", Path("test_dataset"), "test_file")

        self.assertEqual(result, Path("test_dataset/test_file"))
        copy.assert_called_with("tmp", Path("test_dataset/test_file"))
