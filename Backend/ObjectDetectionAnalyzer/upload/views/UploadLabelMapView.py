from pathlib import Path

from ObjectDetectionAnalyzer.settings import DATA_DIR
from ObjectDetectionAnalyzer.upload.views.UploadBaseView import UploadBaseView


class UploadLabelMapView(UploadBaseView):
    """
    Handle requests sent to /upload/label-map/
    """

    def is_file_valid(self, tmp_file_path: Path) -> bool:
        return self.upload_service.is_label_map_valid(tmp_file_path)

    def get_target_dir(self, username, dataset_name):
        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset_name)

        return dataset_dir

    def save_data(self, tmp_file_path, target_dir, dataset_name, dataset, user, file_name):
        label_map_path = self.upload_service.save_data(tmp_file_path, target_dir, "label_map.txt")

        dataset.update(label_map_path=label_map_path)
