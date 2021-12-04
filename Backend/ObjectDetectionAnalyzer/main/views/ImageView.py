import base64

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.main.serializers.ImageSerializer import ImageSerializer
from ObjectDetectionAnalyzer.settings import DATA_DIR


class Image(APIView):
    """
    Handle requests sent to /image
    """

    def get(self, request, image_name):
        """
        Send image based on url.
        """

        with open(DATA_DIR / image_name, mode='rb') as file:
            image_base64 = base64.b64encode(file.read()).decode('utf-8')

        response_data = {
            'name': image_name,
            'file': image_base64
        }

        serializer = ImageSerializer(response_data)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
