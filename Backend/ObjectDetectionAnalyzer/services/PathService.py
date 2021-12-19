from pathlib import Path


class PathService:
    """
    Service for creating paths
    """

    def get_user_dir(self, data_dir: Path, user_name: str) -> Path:
        if data_dir and user_name:
            return Path(data_dir / user_name)

    def create_user_dir(self, user_dir: Path) -> bool:
        if user_dir:
            Path(user_dir).mkdir(parents=True, exist_ok=True)
            return True

        return False
   