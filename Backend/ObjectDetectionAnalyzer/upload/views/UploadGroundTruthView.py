from ObjectDetectionAnalyzer.settings import DATA_DIR
from ObjectDetectionAnalyzer.upload.views.UploadBaseView import UploadBaseView


class UploadGroundTruthView(UploadBaseView):
    """
    View that handles requests sent to /upload/ground-truth.
    """

    def is_file_valid(self, tmp_file_path):
        return self.upload_service.is_ground_truth_valid(tmp_file_path)

    def get_target_dir(self, username, dataset_name, model_name):
        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset_name)

        return dataset_dir

    def save_data(self, tmp_file_path, target_dir, dataset_name, model_name, dataset, model, user, file_name):
        ground_truth_path = self.upload_service.save_data(tmp_file_path, target_dir, "ground_truth.csv")

        dataset.update(ground_truth_path=ground_truth_path)
