from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.services.PathService import PathService
from ObjectDetectionAnalyzer.settings import DATA_DIR


class UploadView(APIView):
    """
    Handle requests sent to /upload
    """
    parser_classes = [MultiPartParser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path_service = PathService()

    def put(self, request, file_name):
        file_obj = request.data['file']

        user_dir = self.path_service.get_user_dir(DATA_DIR, request.user.username)
        self.path_service.create_user_dir(user_dir)

        with open(user_dir / file_name, "wb") as file:
            file.write(file_obj.read())

        return Response(status=status.HTTP_204_NO_CONTENT)
