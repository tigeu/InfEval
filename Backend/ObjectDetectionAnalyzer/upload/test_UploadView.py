import io
from pathlib import Path
from unittest.mock import patch, mock_open

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestUploadView(APITestCase):
    """
    Test UploadView
    """

    def setUp(self):
        self.url = reverse('upload_dataset', kwargs={'file_name': 'test.txt'})
        self.user_dir = Path("dir/test")

    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.create_dir')
    @patch('ObjectDetectionAnalyzer.services.PathService.PathService.get_combined_dir')
    @patch('builtins.open')
    def test_upload_view(self, open, get_combined_dir, create_dir):
        """
        Test that correct image is returned
        """
        open = mock_open()
        get_combined_dir.return_value = self.user_dir
        create_dir.return_value = True

        request = {"file": io.StringIO(),
                   "dataset_name": "test_name"}

        user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=user)

        response = self.client.put(self.url, request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
