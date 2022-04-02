import io
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import PIL.Image

from ObjectDetectionAnalyzer.upload.UploadService import UploadService


class TestUploadService(TestCase):
    """
    Test UploadService
    """

    def setUp(self):
        self.upload_service = UploadService()
        self.files = ["test.csv", "test2.jpg", "test3.png", "test4.c", "test5", "test6.zip"]
        self.saved_model_files = ["test/", "test/something", "saved_model/", "saved_model/model"]

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
        result = self.upload_service.is_prediction_valid(Path("tmp"))

        self.assertEqual(result, True)
        is_valid.assert_called()

    @patch('ObjectDetectionAnalyzer.upload.validators.PyTorchValidator.PyTorchValidator.is_valid')
    def test_is_pytorch_model_valid(self, is_valid):
        is_valid.return_value = True
        result = self.upload_service.is_pytorch_valid(Path("tmp"))

        self.assertEqual(result, True)
        is_valid.assert_called()

    @patch('shutil.rmtree')
    @patch('ObjectDetectionAnalyzer.upload.UploadService.UploadService.save_compressed_model')
    @patch('ObjectDetectionAnalyzer.upload.validators.TensorFlowValidator.TensorFlowValidator.is_valid')
    @patch("zipfile.is_zipfile")
    def test_is_tensorflow_model_valid(self, is_zip_file, is_valid, save_compressed_model, rmtree):
        is_zip_file.return_value = True
        is_valid.return_value = True
        save_compressed_model.return_value = Path("tmp/file")

        result = self.upload_service.is_tf_valid(Path("file"), Path("tmp"))

        self.assertEqual(result, True)
        is_valid.assert_called()

    @patch("zipfile.is_zipfile")
    def test_is_tensorflow_model_valid_without_zip(self, is_zip_file):
        is_zip_file.return_value = False

        result = self.upload_service.is_tf_valid(Path("file"), Path("tmp"))

        self.assertEqual(result, False)

    @patch('ObjectDetectionAnalyzer.upload.UploadService.UploadService.save_compressed_model')
    @patch("zipfile.is_zipfile")
    def test_is_tensorflow_model_valid_without_dir(self, is_zip_file, save_compressed_model):
        is_zip_file.return_value = True
        save_compressed_model.return_value = ""

        result = self.upload_service.is_tf_valid(Path("file"), Path("tmp"))

        self.assertEqual(result, False)

    @patch('ObjectDetectionAnalyzer.upload.validators.YoloValidator.YoloValidator.is_valid')
    def test_is_yolo_model_valid(self, is_valid):
        is_valid.return_value = True
        result = self.upload_service.is_yolo_valid(Path("tmp"), Path("yolov3"))

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

    @patch("zipfile.ZipFile.extract")
    @patch("builtins.open")
    @patch("zipfile.ZipFile")
    @patch("zipfile.is_zipfile")
    def test_save_compressed_model(self, is_zipfile, ZipFile, open, extract):
        is_zipfile.return_value = True
        ZipFile.return_value.__enter__.return_value.namelist.return_value = self.saved_model_files

        result = self.upload_service.save_compressed_model("tmp", "model_dir", "model_name")

        self.assertEqual(result, "model_dir/model_name/saved_model/")

    @patch("zipfile.ZipFile.extract")
    @patch("builtins.open")
    @patch("zipfile.ZipFile")
    @patch("zipfile.is_zipfile")
    @patch("pathlib.Path.unlink")
    @patch("pathlib.Path.is_dir")
    @patch("pathlib.Path.exists")
    def test_save_compressed_model_when_file_saved(self, exists, is_dir, unlink, is_zipfile, ZipFile, open, extract):
        exists.return_value = True
        is_dir.return_value = False
        is_zipfile.return_value = True
        ZipFile.return_value.__enter__.return_value.namelist.return_value = ["some/file", "an/other/file"]

        result = self.upload_service.save_compressed_model("tmp", "model_dir", "model_name")

        self.assertEqual(result, "")

    @patch("zipfile.ZipFile.extract")
    @patch("builtins.open")
    @patch("zipfile.ZipFile")
    @patch("zipfile.is_zipfile")
    def test_save_compressed_model_without_saved_model(self, is_zipfile, ZipFile, open, extract):
        is_zipfile.return_value = True
        ZipFile.return_value.__enter__.return_value.namelist.return_value = ["some/file", "an/other/file"]

        result = self.upload_service.save_compressed_model("tmp", "model_dir", "model_name")

        self.assertEqual(result, "")

    @patch("shutil.copy")
    def test_save_data(self, copy):
        result = self.upload_service.save_data("tmp", Path("test_dataset"), "test_file")

        self.assertEqual(result, Path("test_dataset/test_file"))
        copy.assert_called_with("tmp", Path("test_dataset/test_file"))

    @patch("PIL.Image.open")
    def test_has_invalid_bounding_boxes_valid(self, open):
        open.return_value = PIL.Image.new('RGB', (100, 100))
        values = [
            {'class': 'class1', 'file_name': 'file1.jpg', 'xmin': 0, 'ymin': 0, 'xmax': 100, 'ymax': 100},
            {'class': 'class1', 'file_name': 'file2.png', 'xmin': 25, 'ymin': 25, 'xmax': 100, 'ymax': 100}
        ]
        images = ["path1/file1.jpg", "path2/file2.png"]
        result = self.upload_service.has_invalid_bounding_boxes(values, images)

        self.assertEqual(result, True)

    @patch("PIL.Image.open")
    def test_has_invalid_bounding_boxes_invalid(self, open):
        open.return_value = PIL.Image.new('RGB', (100, 100))
        values = [
            {'class': 'class1', 'file_name': 'file1.jpg', 'xmin': -1, 'ymin': 0, 'xmax': 100, 'ymax': 100},
            {'class': 'class1', 'file_name': 'file2.png', 'xmin': 25, 'ymin': 25, 'xmax': 100, 'ymax': 100}
        ]
        images = ["path1/file1.jpg", "path2/file2.png"]
        result = self.upload_service.has_invalid_bounding_boxes(values, images)

        self.assertEqual(result, False)
