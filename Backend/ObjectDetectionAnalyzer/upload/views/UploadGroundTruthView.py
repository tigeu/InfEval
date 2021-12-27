from pathlib import Path

from ObjectDetectionAnalyzer.settings import DATA_DIR
from ObjectDetectionAnalyzer.upload.views.UploadBaseView import UploadBaseView


class UploadGroundTruthView(UploadBaseView):
    """
    Handle requests sent to /upload/ground-truth/
    """

    def is_file_valid(self, tmp_file_path: Path) -> bool:
        return self.upload_service.is_ground_truth_valid(tmp_file_path)

    def get_target_dir(self, username, dataset_name):
        user_dir = self.path_service.get_combined_dir(DATA_DIR, username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset_name)

        return dataset_dir

    def save_data(self, tmp_file_path, target_dir, dataset_name, dataset, user, file_name):
        ground_truth_path = self.upload_service.save_data(tmp_file_path, target_dir, "ground_truth.csv")

        dataset.update(ground_truth_path=ground_truth_path)

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
        if not self.path_service.create_dir(dataset_dir):
            self.path_service.delete_tmp_file(tmp_file_path)
            return Response("Ground truth directory could not be created", status=status.HTTP_400_BAD_REQUEST)

        ground_truth_path = self.upload_service.save_data(tmp_file_path, dataset_dir, "ground_truth.csv")

        dataset.update(ground_truth_path=ground_truth_path)

        self.path_service.delete_tmp_file(tmp_file_path)

        return Response(status=status.HTTP_204_NO_CONTENT)"""
