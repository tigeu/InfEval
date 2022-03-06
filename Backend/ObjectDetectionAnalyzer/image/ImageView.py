from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.image.ImageSerializer import ImageSerializer
from ObjectDetectionAnalyzer.image.ImageService import ImageService
from ObjectDetectionAnalyzer.services.PathService import PathService
from ObjectDetectionAnalyzer.settings import DATA_DIR


class ImageView(APIView):
    """
    View that handles requests sent to /image.
    GET: Returns the requested image

    Attributes
    ----------
    path_service : PathService
        Service for handling file system tasks
    image_service : ImageService
        Service for encoding image

    Methods
    -------
    get(request)
        Returns the requested image
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        """
        Initialise required services
        """
        super().__init__(**kwargs)
        self.path_service = PathService()
        self.image_service = ImageService()

    def get(self, request, dataset, image_name):
        """
        Send image based on url.
        """
        user_dir = self.path_service.get_combined_dir(DATA_DIR, request.user.username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset)

        image_base64 = self.image_service.encode_image(dataset_dir / image_name)

        if not image_base64:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'name': image_name,
            'file': image_base64
        }

        serializer = ImageSerializer(response_data)

        return Response(serializer.data, status=status.HTTP_200_OK)
