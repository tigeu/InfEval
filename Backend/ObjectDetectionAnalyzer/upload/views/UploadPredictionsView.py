from django.utils import timezone

from ObjectDetectionAnalyzer.settings import DATA_DIR
from ObjectDetectionAnalyzer.upload.UploadModels import Predictions
from ObjectDetectionAnalyzer.upload.views.UploadBaseView import UploadBaseView


class UploadPredictionsView(UploadBaseView):
    """
    View that handles requests sent to /upload/predictions.
    """

    def is_file_valid(self, tmp_file_path):
        return self.upload_service.is_prediction_valid(tmp_file_path)

    def get_target_dir(self, username, dataset_name, model_name):
        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset_name)
        predictions_dir = self.path_service.get_predictions_dir(dataset_dir)

        return predictions_dir

    def save_data(self, tmp_file_path, target_dir, dataset_name, model_name, dataset, model, user, file_name):
        predictions_path = self.upload_service.save_data(tmp_file_path, target_dir, file_name)
        prediction = Predictions.objects.filter(name=file_name, userId=user)
        if prediction:
            prediction.update(uploaded_at=timezone.now())
        else:
            dataset_instance = dataset.first()
            Predictions.objects.create(name=file_name, path=predictions_path, datasetId=dataset_instance, userId=user)
