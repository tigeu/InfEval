from pathlib import Path

from django.utils import timezone

from ObjectDetectionAnalyzer.settings import DATA_DIR
from ObjectDetectionAnalyzer.upload.UploadModels import Predictions
from ObjectDetectionAnalyzer.upload.views.UploadBaseView import UploadBaseView


class UploadPredictionsView(UploadBaseView):
    """
    Handle requests sent to /upload/predictions/
    """

    def is_file_valid(self, tmp_file_path: Path) -> bool:
        return self.upload_service.is_ground_truth_valid(tmp_file_path)

    def get_target_dir(self, username, dataset_name):
        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset_name)
        predictions_dir = self.path_service.get_predictions_dir(dataset_dir)

        return predictions_dir

    def save_data(self, tmp_file_path, target_dir, dataset_name, dataset, user, file_name):
        predictions_path = self.upload_service.save_data(tmp_file_path, target_dir, file_name)
        prediction = Predictions.objects.filter(name=file_name, userId=user)
        if prediction:
            prediction.update(uploaded_at=timezone.now())
        else:
            dataset_instance = dataset.first()
            Predictions.objects.create(name=file_name, path=predictions_path, datasetId=dataset_instance, userId=user)

    """def put(self, request, file_name):
        username = request.user.username
        file_obj = request.data['file']
        dataset_name = request.data['dataset_name']

        tmp_file_path = self.path_service.save_tmp_file(TMP_DIR, file_name, file_obj)
        if not tmp_file_path:
            return Response("File could not be saved", status=status.HTTP_400_BAD_REQUEST)

        dataset = Dataset.objects.filter(name=dataset_name, userId=request.user)
        if not dataset:
            self.path_service.delete_tmp_file(tmp_file_path)
            return Response("Dataset does not exist yet", status=status.HTTP_400_BAD_REQUEST)

        if not self.upload_service.is_ground_truth_valid(tmp_file_path):
            self.path_service.delete_tmp_file(tmp_file_path)
            return Response("Invalid file uploaded", status=status.HTTP_400_BAD_REQUEST)

        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset_name)
        predictions_dir = self.path_service.get_predictions_dir(dataset_dir)
        if not self.path_service.create_dir(predictions_dir):
            self.path_service.delete_tmp_file(tmp_file_path)
            return Response("Predictions directory could not be created", status=status.HTTP_400_BAD_REQUEST)

        predictions_path = self.upload_service.save_data(tmp_file_path, predictions_dir, file_name)

        prediction = Predictions.objects.filter(name=file_name, userId=request.user)
        if prediction:
            prediction.update(uploaded_at=timezone.now())
        else:
            dataset_instance = dataset.first()
            Predictions.objects.create(name=file_name, path=predictions_path, datasetId=dataset_instance,
                                       userId=request.user)

        self.path_service.delete_tmp_file(tmp_file_path)

        return Response(status=status.HTTP_204_NO_CONTENT)"""
