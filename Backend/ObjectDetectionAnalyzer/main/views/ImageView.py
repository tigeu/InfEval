from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.main.serializers.ImageSerializer import ImageSerializer
from ObjectDetectionAnalyzer.main.services.FileService import FileService
from ObjectDetectionAnalyzer.settings import DATA_DIR


class Image(APIView):
    """
    Handle requests sent to /image
    """

    def get(self, request, image_name):
        """
        Send image based on url.
        """
        image_base64 = FileService().encode_image(DATA_DIR / image_name)

        if not image_base64:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'name': image_name,
            'file': image_base64
        }

        serializer = ImageSerializer(response_data)

        return Response(serializer.data, status=status.HTTP_200_OK)
