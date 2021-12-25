import os
import shutil
import zipfile

from ObjectDetectionAnalyzer.upload.DatasetModel import Dataset
from ObjectDetectionAnalyzer.upload.UploadFileTypes import UploadFileTypes
from ObjectDetectionAnalyzer.upload.UploadTypes import UploadTypes


class UploadService:
    """
    Service for checking file and saving uploaded data
    """

    def is_file_valid(self, file_type, upload_type, tmp_file_path) -> bool:
        if file_type not in set(item.value for item in UploadFileTypes):
            return False

        if upload_type not in set(item.value for item in UploadTypes):
            return False

        if file_type == UploadFileTypes.COMPRESSED.value and upload_type == UploadTypes.DATASET.value:
            return zipfile.is_zipfile(tmp_file_path)

        return False

    def save_file_data(self, tmp_file_path, dataset_dir, dataset_name, upload_type, user):
        ground_truth_path = ""
        label_map_path = ""
        if upload_type == UploadTypes.DATASET.value:
            with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    filename = os.path.basename(member)
                    if not filename:
                        continue  # skip directory
                    source = zip_ref.open(member)
                    target = open(os.path.join(dataset_dir, filename), "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)

        Dataset.objects.create(name=dataset_name,
                               path=dataset_dir,
                               ground_truth_path=ground_truth_path,
                               label_map_path=label_map_path,
                               userId=user)
