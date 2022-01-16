from pathlib import Path
from unittest.mock import patch

from PIL import Image
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.upload.UploadModels import Dataset


class TestGroundTruthView(APITestCase):
    """
    Test GroundTruthView
    """

    def setUp(self):
        self.url = reverse('ground-truth', kwargs={'dataset': 'test_dataset', 'image_name': 'test_image.jpg'})
        self.user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=self.user)
        self.settings = {"stroke_size": 15, "show_colored": "true", "show_labeled": "true", "font_size": 35}

    def test_ground_truth_view_without_dataset(self):
        """
        Test that 404 is sent with a message
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Dataset does not exist yet")

    def test_ground_truth_view_without_ground_truth(self):
        """
        Test that 404 is sent with a message
        """
        Dataset.objects.create(name="test_dataset", path=Path(), userId=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Ground truth file for dataset does not exist yet")

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_files_from_dir')
    def test_ground_truth_view_without_correct_image(self, get_files_from_dir):
        """
        Test that 404 is sent with a message
        """
        get_files_from_dir.return_value = ["test_image1.jpg", "test_image2.png"]

        Dataset.objects.create(name="test_dataset", ground_truth_path=Path("some_path"), userId=self.user)

        response = self.client.get(self.url, data=self.settings)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Image not found in dataset")

    @patch('ObjectDetectionAnalyzer.groundtruth.DrawBoundingBoxService.DrawBoundingBoxService.draw_bounding_boxes')
    @patch('ObjectDetectionAnalyzer.services.CSVParseService.CSVParseService.get_classes')
    @patch('ObjectDetectionAnalyzer.services.CSVParseService.CSVParseService.get_values_for_image')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_files_from_dir')
    def test_ground_truth_view_with_correct_image(self, get_files_from_dir, get_values_for_image, get_classes,
                                                  draw_bounding_boxes):
        """
        Test that 404 is sent with a message
        """
        get_files_from_dir.return_value = ["test_image.jpg", "test_image2.png"]
        values = [{'class': 'class1', 'xmin': 0, 'ymin': 0, 'xmax': 10, 'ymax': 10}]
        get_values_for_image.return_value = values
        get_classes.return_value = ['class1']
        draw_bounding_boxes.return_value = Image.new('RGBA', (100, 100), (255, 0, 0, 0))

        Dataset.objects.create(name="test_dataset", ground_truth_path=Path("some_path"), userId=self.user)

        response = self.client.get(self.url, data=self.settings)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_image.jpg')
