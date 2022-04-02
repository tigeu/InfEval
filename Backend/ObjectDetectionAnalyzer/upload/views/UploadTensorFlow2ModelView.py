from django.utils import timezone

from ObjectDetectionAnalyzer.settings import DATA_DIR, TMP_DIR
from ObjectDetectionAnalyzer.upload.ModelTypes import ModelTypes
from ObjectDetectionAnalyzer.upload.UploadModels import Models
from ObjectDetectionAnalyzer.upload.views.UploadBaseView import UploadBaseView


class UploadTensorFlow2ModelView(UploadBaseView):
    """
    View that handles requests sent to /upload/tf2.
    """

    def requires_dataset(self):
        return False

    def is_file_valid(self, tmp_file_path, dataset=None):
        return self.upload_service.is_tf_valid(tmp_file_path, TMP_DIR)

    def get_target_dir(self, username, dataset_name, model_name):
        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        model_dir = self.path_service.get_model_dir(user_dir, model_name)

        return model_dir

    def save_data(self, tmp_file_path, target_dir, dataset_name, model_name, dataset, model, user, file_name):
        model_type = ModelTypes.TENSORFLOW2.value
        model_path = self.upload_service.save_compressed_model(tmp_file_path, target_dir, model_name)
        model = Models.objects.filter(name=model_name, userId=user)
        if model:
            model.update(path=model_path, type=model_type, uploaded_at=timezone.now())
        else:
            Models.objects.create(name=model_name, path=model_path, type=model_type, userId=user)
