from pathlib import Path

from django.utils import timezone

from ObjectDetectionAnalyzer.settings import DATA_DIR
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset
from ObjectDetectionAnalyzer.upload.views.UploadBaseView import UploadBaseView


class UploadDatasetView(UploadBaseView):
    def requires_dataset(self):
        return False

    def is_file_valid(self, tmp_file_path: Path) -> bool:
        return self.upload_service.is_zip_valid(tmp_file_path)

    def get_target_dir(self, username: str, dataset_name: str):
        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset_name)

        return dataset_dir

    def create_dir(self, directory: Path) -> bool:
        return self.path_service.create_dir(directory, True)

    def save_data(self, tmp_file_path, target_dir, dataset_name, dataset, user, file_name):
        self.upload_service.save_compressed_data(tmp_file_path, target_dir)
        dataset = Dataset.objects.filter(name=dataset_name, userId=user)
        if dataset:
            dataset.update(uploaded_at=timezone.now())
        else:
            Dataset.objects.create(name=dataset_name, path=target_dir, userId=user)
