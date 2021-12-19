from pathlib import PosixPath, Path
from unittest import TestCase

from ObjectDetectionAnalyzer.services.PathService import PathService


class TestPathService(TestCase):
    """
    Test PathService
    """

    # Path(user_dir).mkdir(parents=True, exist_ok=True)
    def setUp(self):
        self.path_service = PathService()
        self.directory = PosixPath("dir")
        self.user_name = "user"

    def test_path_service_get_user_dir(self):
        user_dir = self.path_service.get_user_dir(self.directory, self.user_name)

        self.assertEqual(user_dir, Path("dir/user"))

    def test_path_service_get_user_dir_without_user_name(self):
        user_dir = self.path_service.get_user_dir(self.directory, "")

        self.assertEqual(user_dir, None)

    def test_path_service_get_user_dir_without_directory(self):
        user_dir = self.path_service.get_user_dir("", self.user_name)

        self.assertEqual(user_dir, None)

    def test_create_user_dir(self):
        result = self.path_service.create_user_dir(Path(self.directory))
        self.assertEqual(result, True)

    def test_create_user_dir_without_dir(self):
        result = self.path_service.create_user_dir(None)
        self.assertEqual(result, False)
