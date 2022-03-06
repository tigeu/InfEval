from ObjectDetectionAnalyzer.settings import DATA_DIR
from ObjectDetectionAnalyzer.upload.views.UploadBaseView import UploadBaseView


class UploadLabelMapView(UploadBaseView):
    """
    View that handles requests sent to /upload/label-map.
    """

    def requires_dataset(self):
        return False

    def requires_model(self):
        return True

    def is_file_valid(self, tmp_file_path):
        return self.upload_service.is_label_map_valid(tmp_file_path)

    def get_target_dir(self, username, dataset_name, model_name):
        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        model_dir = self.path_service.get_model_dir(user_dir, model_name)

        return model_dir

    def save_data(self, tmp_file_path, target_dir, dataset_name, model_name, dataset, model, user, file_name):
        label_map_path = self.upload_service.save_data(tmp_file_path, target_dir, "label_map.txt")

        model.update(label_map_path=label_map_path)
