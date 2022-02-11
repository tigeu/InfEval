from pathlib import Path

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.services.PathService import PathService
from ObjectDetectionAnalyzer.settings import TMP_DIR
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Models
from ObjectDetectionAnalyzer.upload.UploadService import UploadService


class UploadBaseView(APIView):
    parser_classes = [MultiPartParser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path_service = PathService()
        self.upload_service = UploadService()

    def requires_dataset(self):
        return True

    def requires_model(self):
        return False

    def is_file_valid(self, tmp_file_path: Path) -> bool:
        pass

    def get_target_dir(self, username, dataset_name, model_name):
        pass

    def create_dir(self, dir: Path) -> bool:
        return self.path_service.create_dir(dir, False)

    def save_data(self, tmp_file_path, target_dir, dataset_name, model_name, dataset, model, user, file_name):
        pass

    def put(self, request, file_name):
        user = request.user
        username = user.username
        file_obj = request.data['file']
        dataset_name = request.data['dataset_name']
        model_name = request.data['model_name']

        tmp_file_path = self.path_service.save_tmp_file(TMP_DIR, file_name, file_obj)
        if not tmp_file_path:
            return Response("File could not be saved", status=status.HTTP_400_BAD_REQUEST)

        dataset = Dataset.objects.filter(name=dataset_name, userId=user)
        if self.requires_dataset():
            if not dataset:
                self.path_service.delete_tmp_file(tmp_file_path)
                return Response("Dataset does not exist yet", status=status.HTTP_400_BAD_REQUEST)

        model = Models.objects.filter(name=model_name, userId=user)
        if self.requires_model():
            if not model:
                self.path_service.delete_tmp_file(tmp_file_path)
                return Response("Model does not exist yet", status=status.HTTP_400_BAD_REQUEST)

        if not self.is_file_valid(tmp_file_path):
            self.path_service.delete_tmp_file(tmp_file_path)
            return Response("Invalid file uploaded", status=status.HTTP_400_BAD_REQUEST)

        target_dir = self.get_target_dir(username, dataset_name, model_name)
        if not self.create_dir(target_dir):
            self.path_service.delete_tmp_file(tmp_file_path)
            return Response("Dataset directory could not be created", status=status.HTTP_400_BAD_REQUEST)

        self.save_data(tmp_file_path, target_dir, dataset_name, model_name, dataset, model, user, file_name)
        self.path_service.delete_tmp_file(tmp_file_path)

        return Response(status=status.HTTP_204_NO_CONTENT)
