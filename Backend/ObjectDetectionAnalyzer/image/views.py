from pathlib import Path

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.image.serializers import ImageSerializer
from ObjectDetectionAnalyzer.image.services import ImageService
from ObjectDetectionAnalyzer.settings import DATA_DIR


class Image(APIView):
    """
    Handle requests sent to /image
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, image_name):
        """
        Send image based on url.
        """
        user_dir = DATA_DIR / request.user.username
        Path(user_dir).mkdir(parents=True, exist_ok=True)

        image_base64 = ImageService().encode_image(user_dir / image_name)

        if not image_base64:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'name': image_name,
            'file': image_base64
        }

        serializer = ImageSerializer(response_data)

        return Response(serializer.data, status=status.HTTP_200_OK)
