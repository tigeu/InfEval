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
    View that handles requests sent to /image-files.
    GET: Returns a list of all image file names in a given dataset

    Attributes
    ----------
    path_service : PathService
        Service for handling file system tasks
    image_file_service : ImageFilesService
        Service for retrieving all image file names for a given dataset

    Methods
    -------
    get(request)
        Returns a list of all image file names in a given dataset
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        """
        Initialise required services
        """
        super().__init__(**kwargs)
        self.path_service = PathService()
        self.image_file_service = ImageFilesService()

    def get(self, request, dataset):
        """
        Returns a list of all image file names in a given dataset

        Parameters
        ----------
        request : HttpRequest
            GET request
        dataset : str
            Dataset name for which the image file names are requestred

        Returns
        -------
        Response
            Requested data with status code
        """
        user_dir = self.path_service.get_combined_dir(DATA_DIR, request.user.username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset)

        image_names = self.image_file_service.get_image_file_names(dataset_dir, IMAGE_ENDINGS)

        if not image_names:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        response_data = [
            {'name': image_name} for image_name in image_names
        ]

        serializer = ImageFilesSerializer(response_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
