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

    def get_target_dir(self, username, dataset_name):
        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset_name)

        return dataset_dir

    def create_dir(self, dir: Path) -> bool:
        return self.path_service.create_dir(dir, True)

    def save_data(self, tmp_file_path, target_dir, dataset_name, dataset, user, file_name):
        self.upload_service.save_compressed_data(tmp_file_path, target_dir)
        dataset = Dataset.objects.filter(name=dataset_name, userId=user)
        if dataset:
            dataset.update(uploaded_at=timezone.now())
        else:
            Dataset.objects.create(name=dataset_name, path=target_dir, userId=user)

    """
    Handle requests sent to /upload/dataset/
    """

    """def put(self, request, file_name):
        username = request.user.username
        file_obj = request.data['file']
        dataset_name = request.data['dataset_name']

        tmp_file_path = self.path_service.save_tmp_file(TMP_DIR, file_name, file_obj)
        if not tmp_file_path:
            return Response("File could not be saved", status=status.HTTP_400_BAD_REQUEST)

        if not self.upload_service.is_zip_valid(tmp_file_path):
            self.path_service.delete_tmp_file(tmp_file_path)
            return Response("Invalid file uploaded", status=status.HTTP_400_BAD_REQUEST)

        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset_name)
        if not self.path_service.create_dir(dataset_dir, True):
            self.path_service.delete_tmp_file(tmp_file_path)
            return Response("Dataset directory could not be created", status=status.HTTP_400_BAD_REQUEST)

        self.upload_service.save_compressed_data(tmp_file_path, dataset_dir)
        dataset = Dataset.objects.filter(name=dataset_name, userId=request.user)
        if dataset:
            dataset.update(uploaded_at=timezone.now())
        else:
            Dataset.objects.create(name=dataset_name, path=dataset_dir, userId=request.user)

        self.path_service.delete_tmp_file(tmp_file_path)

        return Response(status=status.HTTP_204_NO_CONTENT)
"""
