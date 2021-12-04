import os

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.main.serializers.ImageFilesSerializer import ImageFilesSerializer
from ObjectDetectionAnalyzer.settings import DATA_DIR, IMAGE_ENDINGS


class ImageFiles(APIView):
    """
    Handle requests sent to /image-files
    """

    def get(self, request):
        """
        Send image with name image_name from data directory.
        """
        all_file_names = os.listdir(DATA_DIR)
        image_names = []
        for file_name in all_file_names:
            base_name = os.path.basename(file_name)
            extension = os.path.splitext(file_name)[1]
            if extension.lower() in IMAGE_ENDINGS:
                image_names.append(base_name)

        response_data = [
            {'name': image_name} for image_name in image_names
        ]

        serializer = ImageFilesSerializer(response_data, many=True)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
