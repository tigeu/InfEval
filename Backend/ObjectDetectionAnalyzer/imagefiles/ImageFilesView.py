from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.imagefiles.ImageFilesSerializer import ImageFilesSerializer
from ObjectDetectionAnalyzer.imagefiles.ImageFilesService import ImageFilesService
from ObjectDetectionAnalyzer.services.PathService import PathService
from ObjectDetectionAnalyzer.settings import DATA_DIR, IMAGE_ENDINGS


class ImageFilesView(APIView):
    """
    Handle requests sent to /image-files
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path_service = PathService()
        self.image_file_service = ImageFilesService()

    def get(self, request):
        """
        Send image with name image_name from data directory.
        """
        user_dir = self.path_service.get_user_dir(DATA_DIR, request.user.username)
        self.path_service.create_user_dir(user_dir)

        image_names = self.image_file_service.get_image_file_names(user_dir, IMAGE_ENDINGS)

        if not image_names:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        response_data = [
            {'name': image_name} for image_name in image_names
        ]

        serializer = ImageFilesSerializer(response_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
