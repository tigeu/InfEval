from pathlib import Path


class PathService:
    """
    Service for creating paths
    """

    def get_user_dir(self, data_dir, user_name):
        user_dir = data_dir / user_name
        Path(user_dir).mkdir(parents=True, exist_ok=True)

        return user_dir
