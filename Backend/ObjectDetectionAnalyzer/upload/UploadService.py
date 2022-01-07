import os
import shutil
import zipfile
from pathlib import Path

from ObjectDetectionAnalyzer.upload.validators.GroundTruthValidator import GroundTruthValidator
from ObjectDetectionAnalyzer.upload.validators.LabelMapValidator import LabelMapValidator
from ObjectDetectionAnalyzer.upload.validators.ModelValidator import ModelValidator
from ObjectDetectionAnalyzer.upload.validators.PredictionsValidator import PredictionsValidator


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
                if ext in image_endings:
                    contains_image = True
                    break
        return contains_image

    def is_ground_truth_valid(self, tmp_file_path: Path) -> bool:
        return GroundTruthValidator().is_valid(tmp_file_path)

    def is_label_map_valid(self, tmp_file_path: Path) -> bool:
        return LabelMapValidator().is_valid(tmp_file_path)

    def is_prediction_valid(self, tmp_file_path: Path) -> bool:
        return PredictionsValidator().is_valid(tmp_file_path)

    def is_model_valid(self, tmp_file_path: Path) -> bool:
        return ModelValidator().is_valid(tmp_file_path)

    def save_compressed_data(self, tmp_file_path, dataset_dir, image_endings):
        with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                _, ext = os.path.splitext(member)
                if ext not in image_endings:
                    continue  # skip non-image files
                filename = os.path.basename(member)
                source = zip_ref.open(member)
                target = open(os.path.join(dataset_dir, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)

    def save_data(self, tmp_file_path, target_dir, file_name):
        path = target_dir / file_name
        shutil.copy(tmp_file_path, path)

        return path
