from django.utils import timezone

from ObjectDetectionAnalyzer.settings import DATA_DIR, IMAGE_ENDINGS
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions
from ObjectDetectionAnalyzer.upload.views.UploadBaseView import UploadBaseView


class UploadDatasetView(UploadBaseView):
    """
    View that handles requests sent to /upload/dataset.
    """

    def requires_dataset(self):
        return False

    def is_file_valid(self, tmp_file_path, dataset=None):
        return self.upload_service.is_zip_valid(tmp_file_path, IMAGE_ENDINGS)

    def get_target_dir(self, username, dataset_name, model_name):
        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset_name)

        return dataset_dir

    def create_dir(self, directory):
        return self.path_service.create_dir(directory, True)

    def save_data(self, tmp_file_path, target_dir, dataset_name, model_name, dataset, model, user, file_name):
        self.upload_service.save_compressed_data(tmp_file_path, target_dir, IMAGE_ENDINGS)
        dataset = Dataset.objects.filter(name=dataset_name, userId=user)
        if dataset:
            dataset.update(ground_truth_path="", uploaded_at=timezone.now())
            predictions = Predictions.objects.filter(datasetId=dataset.first(), userId=user)
            if predictions:
                predictions.delete()
        else:
            Dataset.objects.create(name=dataset_name, path=target_dir, userId=user)
