from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.main.serializers.ImageFilesSerializer import ImageFilesSerializer
from ObjectDetectionAnalyzer.main.services.FileService import FileService
from ObjectDetectionAnalyzer.settings import DATA_DIR, IMAGE_ENDINGS


class ImageFiles(APIView):
    """
    Handle requests sent to /image-files
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Send image with name image_name from data directory.
        """
        image_names = FileService().get_image_file_names(DATA_DIR, IMAGE_ENDINGS)

        if not image_names:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        response_data = [
            {'name': image_name} for image_name in image_names
        ]

        serializer = ImageFilesSerializer(response_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
