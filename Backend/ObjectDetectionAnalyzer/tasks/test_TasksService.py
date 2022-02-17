from unittest import TestCase

from ObjectDetectionAnalyzer.tasks.TasksService import TasksService


class TestTasksService(TestCase):
    def setUp(self):
        self.tasks_service = TasksService()
        self.label_map = {"1": "class1", "2": "class2"}

    def test_replace_class_names(self):
        predictions = {"image1": [{"class": "1"}, {"class": "1"}, {"class": "2"}],
                       "image2": [{"class": "1"}, {"class": "3"}, {"class": "3"}],
                       "image3": [{"class": "2"}, {"class": "2"}, {"class": "2"}]}

        expected = {"image1": [{"class": "class1"}, {"class": "class1"}, {"class": "class2"}],
                    "image2": [{"class": "class1"}, {"class": "3"}, {"class": "3"}],
                    "image3": [{"class": "class2"}, {"class": "class2"}, {"class": "class2"}]}

        self.tasks_service.replace_class_names(predictions, self.label_map)

        self.assertEqual(predictions, expected)
