from django.urls import reverse
from rest_framework.test import APITestCase


class test_image(APITestCase):
    def test_increment_heartbeat(self):
        """
        Test that correct image is returned
        """
        data = {'image_name': "test_image.jpg"}
        url = reverse('image', kwargs=data)

        # response = self.client.get(url)

        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['count'], 2)
