import os
import shutil
import zipfile
from pathlib import Path

from ObjectDetectionAnalyzer.upload.validators.GroundTruthValidator import GroundTruthValidator
from ObjectDetectionAnalyzer.upload.validators.LabelMapValidator import LabelMapValidator
from ObjectDetectionAnalyzer.upload.validators.PredictionsValidator import PredictionsValidator
from ObjectDetectionAnalyzer.upload.validators.PyTorchValidator import PyTorchValidator
from ObjectDetectionAnalyzer.upload.validators.TensorFlowValidator import TensorFlowValidator
from ObjectDetectionAnalyzer.upload.validators.YoloValidator import YoloValidator


class UploadService:
    """
    Service for checking file and saving uploaded data
    """

    def is_zip_valid(self, tmp_file_path: Path, image_endings: set) -> bool:
        contains_image = False
        if not zipfile.is_zipfile(tmp_file_path):
            return False

        with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                _, ext = os.path.splitext(file)
                if ext.lower() in image_endings:
                    contains_image = True
                    break
        return contains_image

    def is_ground_truth_valid(self, tmp_file_path: Path) -> bool:
        return GroundTruthValidator().is_valid(tmp_file_path)

    def is_label_map_valid(self, tmp_file_path: Path) -> bool:
        return LabelMapValidator().is_valid(tmp_file_path)

    def is_prediction_valid(self, tmp_file_path: Path) -> bool:
        return PredictionsValidator().is_valid(tmp_file_path)

    def is_pytorch_valid(self, tmp_file_path: Path) -> bool:
        return PyTorchValidator().is_valid(tmp_file_path)

    def is_tf_valid(self, tmp_file_path: Path, tmp_dir: Path, is_tensor_flow_1: bool = False) -> bool:
        dir = self.save_compressed_model(tmp_file_path, tmp_dir, "")
        is_valid = TensorFlowValidator().is_valid(dir, is_tensor_flow_1)
        shutil.rmtree(dir)

        return is_valid

    def is_yolo_valid(self, yolo_dir: Path, tmp_file_path: Path):
        return YoloValidator().is_valid(yolo_dir, tmp_file_path)

    def save_compressed_data(self, tmp_file_path, dataset_dir, image_endings):
        with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                _, ext = os.path.splitext(member)
                if ext.lower() not in image_endings:
                    continue  # skip non-image files
                filename = os.path.basename(member)
                source = zip_ref.open(member)
                target = open(os.path.join(dataset_dir, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)

    def save_compressed_model(self, tmp_file_path, model_dir, model_name):
        target_path = os.path.join(model_dir, model_name)
        with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if 'saved_model/' in file:
                    zip_ref.extract(file, target_path)

        return os.path.join(target_path, "saved_model/")

    def save_data(self, tmp_file_path, target_dir, file_name):
        path = target_dir / file_name
        shutil.copy(tmp_file_path, path)

        return path
