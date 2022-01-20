from unittest import TestCase

from ObjectDetectionAnalyzer.services.ColorService import ColorService


class TestColorService(TestCase):
    """
    Test ColorService
    """

    def setUp(self):
        self.color_service = ColorService()

    def test_get_class_colors(self):
        classes = ["class1", "class2", "class3"]

        colors = self.color_service.get_class_colors(classes)

        self.assertEqual(colors, ["#1CE6FF", "#FF34FF", "#FF4A46"])
