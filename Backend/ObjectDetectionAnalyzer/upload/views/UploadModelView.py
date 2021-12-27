from pathlib import Path

from django.utils import timezone

from ObjectDetectionAnalyzer.settings import DATA_DIR
from ObjectDetectionAnalyzer.upload.UploadModels import Models
from ObjectDetectionAnalyzer.upload.views.UploadBaseView import UploadBaseView


class UploadModelView(UploadBaseView):
    """
    Handle requests sent to /upload/model/
    """

    def requires_dataset(self):
        return False

    def is_file_valid(self, tmp_file_path: Path) -> bool:
        return self.upload_service.is_model_valid(tmp_file_path)

    def get_target_dir(self, username, dataset_name):
        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        model_dir = self.path_service.get_model_dir(user_dir)

        return model_dir

    def save_data(self, tmp_file_path, target_dir, dataset_name, dataset, user, file_name):
        model_path = self.upload_service.save_data(tmp_file_path, target_dir, file_name)
        model = Models.objects.filter(name=file_name, userId=user)
        if model:
            model.update(uploaded_at=timezone.now())
        else:
            Models.objects.create(name=file_name, path=model_path, userId=user)

    """def put(self, request, file_name):
        username = request.user.username
        file_obj = request.data['file']
        dataset_name = request.data['dataset_name']

        tmp_file_path = self.path_service.save_tmp_file(TMP_DIR, file_name, file_obj)
        if not tmp_file_path:
            return Response("File could not be saved", status=status.HTTP_400_BAD_REQUEST)

        if not self.upload_service.is_model_valid(tmp_file_path):
            self.path_service.delete_tmp_file(tmp_file_path)
            return Response("Invalid file uploaded", status=status.HTTP_400_BAD_REQUEST)

        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        model_dir = self.path_service.get_model_dir(user_dir)
        if not self.path_service.create_dir(model_dir):
            self.path_service.delete_tmp_file(tmp_file_path)
            return Response("Ground truth directory could not be created", status=status.HTTP_400_BAD_REQUEST)

        model_path = self.upload_service.save_data(tmp_file_path, model_dir, file_name)
        model = Models.objects.filter(name=file_name, userId=request.user)
        if model:
            model.update(uploaded_at=timezone.now())
        else:
            Models.objects.create(name=file_name, path=model_path, userId=request.user)

        self.path_service.delete_tmp_file(tmp_file_path)

        return Response(status=status.HTTP_204_NO_CONTENT)"""
