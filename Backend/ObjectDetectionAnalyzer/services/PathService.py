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

    def save_tmp_file(self, tmp_file_path: Path, file_obj: any):
        with open(tmp_file_path, "wb") as file:
            file.write(file_obj.read())

    def delete_tmp_file(self, tmp_file_path):
        Path.unlink(tmp_file_path)

    def get_dataset_dir(self, user_dir, dataset_name):
        dataset_dir = user_dir / dataset_name
        if user_dir and dataset_name:
            return Path(user_dir / dataset_name)
