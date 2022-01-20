from unittest.mock import patch

from PIL import Image
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions


class TestPredictionView(APITestCase):
    def setUp(self):
        self.url = reverse('prediction', kwargs={'dataset': 'dataset', 'prediction': 'pred', 'image_name': 'image.jpg'})
        self.user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=self.user)
        self.settings = {"stroke_size": 15, "show_colored": "true", "show_labeled": "true", "font_size": 35,
                         "classes": ["class", "class2"], "colors": ["color1", "color2"]}

    def test_prediction_view_without_dataset(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Dataset does not exist yet")

    def test_ground_truth_view_without_ground_truth(self):
        Dataset.objects.create(name="dataset", userId=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Prediction file does not exist yet")

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_files_from_dir')
    def test_ground_truth_view_without_correct_image(self, get_files_from_dir):
        get_files_from_dir.return_value = ["test_image1.jpg", "test_image2.png"]

        dataset = Dataset.objects.create(name="dataset", userId=self.user)
        Predictions.objects.create(name="pred", datasetId=dataset, userId=self.user)

        response = self.client.get(self.url, data=self.settings)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Image not found in dataset")

    @patch('ObjectDetectionAnalyzer.services.DrawBoundingBoxService.DrawBoundingBoxService.draw_bounding_boxes')
    @patch('ObjectDetectionAnalyzer.services.CSVParseService.CSVParseService.get_values_for_image')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_files_from_dir')
    def test_ground_truth_view_with_correct_image(self, get_files_from_dir, get_values_for_image, draw_bounding_boxes):
        get_files_from_dir.return_value = ["image.jpg", "image2.png"]
        values = [{'class': 'class1', 'confidence': 50, 'xmin': 0, 'ymin': 0, 'xmax': 10, 'ymax': 10}]
        get_values_for_image.return_value = values
        draw_bounding_boxes.return_value = Image.new('RGBA', (100, 100), (255, 0, 0, 0))

        dataset = Dataset.objects.create(name="dataset", userId=self.user)
        Predictions.objects.create(name="pred", datasetId=dataset, userId=self.user)

        response = self.client.get(self.url, data=self.settings)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'image.jpg')
