import shutil
from pathlib import Path


class PathService:
    """
    Service for creating paths
    """

    def get_combined_dir(self, path: Path, name: str) -> Path:
        if path and name:
            return Path(path / name)

    def create_dir(self, dir: Path, recreate=False) -> bool:
        if recreate and dir.is_dir():
            shutil.rmtree(dir)

        if dir:
            Path(dir).mkdir(parents=True, exist_ok=True)
            return True

        return False

    def get_dataset_dir(self, user_dir, dataset_name):
        if user_dir and dataset_name:
            dataset_dir = user_dir / "datasets" / dataset_name
            return Path(dataset_dir)

    def get_predictions_dir(self, dataset_dir):
        if dataset_dir:
            predictions_dir = dataset_dir / "predictions"
            return Path(predictions_dir)

    def get_model_dir(self, user_dir):
        if user_dir:
            model_dir = user_dir / "models"
            return Path(model_dir)

    def save_tmp_file(self, tmp_dir: Path, file_name: str, file_obj: any) -> Path:
        if self.create_dir(tmp_dir):
            tmp_file_path = self.get_combined_dir(tmp_dir, file_name)
            with open(tmp_file_path, "wb") as file:
                file.write(file_obj.read())
            return tmp_file_path

    def delete_tmp_file(self, tmp_file_path):
        Path.unlink(tmp_file_path)
