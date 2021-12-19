from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestHeartbeatView(APITestCase):
    def test_increment_heartbeat(self):
        """
        Test that an incoming number is incremented and sent back with code 200
        """
        data = {'count': 1}
        url = reverse('heartbeat', kwargs=data)

        user = User.objects.create_user("test", "test@test.test", "test")
        self.client.force_authenticate(user=user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_no_authentication_heartbeat(self):
        """
        Test that user without authentication gets 401
        """
        data = {'count': 1}
        url = reverse('heartbeat', kwargs=data)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
