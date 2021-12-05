from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class test_heartbeat(APITestCase):
    def test_increment_heartbeat(self):
        """
        Test that an incoming number is incremented and sent back with code 200
        """
        data = {'count': 1}
        url = reverse('heartbeat', kwargs=data)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
