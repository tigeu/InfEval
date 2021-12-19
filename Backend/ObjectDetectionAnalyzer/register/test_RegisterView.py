from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestRegisterView(APITestCase):
    """
    Test RegisterView
    """

    def setUp(self):
        self.url = reverse('register')

    @patch('django.contrib.auth.models.UserManager.create_user')
    def test_register_with_user(self, create_user):
        """
        Test that registration is successful
        """
        request = {"username": "test",
                   "email": "test@test.test",
                   "password": "test"}

        response = self.client.post(self.url, request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_user.call_count, 1)

    @patch('django.contrib.auth.models.UserManager.create_user')
    def test_register_with_invalid_email(self, create_user):
        """
        Test that registration does not work
        """
        request = {"username": "test",
                   "email": "test",
                   "password": "test"}

        response = self.client.post(self.url, request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(create_user.call_count, 0)

    @patch('django.contrib.auth.models.UserManager.create_user')
    def test_register_with_missing_user(self, create_user):
        """
        Test that registration does not work
        """
        request = {"email": "test",
                   "password": "test"}

        response = self.client.post(self.url, request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(create_user.call_count, 0)
