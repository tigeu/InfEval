from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.services.PathService import PathService
from ObjectDetectionAnalyzer.settings import TMP_DIR, DATA_DIR
from ObjectDetectionAnalyzer.upload.UploadService import UploadService


class UploadView(APIView):
    """
    Handle requests sent to /upload
    """
    parser_classes = [MultiPartParser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path_service = PathService()
        self.upload_service = UploadService()

    def put(self, request, file_name):
        file_obj = request.data['file']
        file_type = file_obj.content_type
        dataset_name = request.data['dataset_name']
        upload_type = int(request.data['type'])

        self.path_service.create_dir(TMP_DIR)
        tmp_file_path = self.path_service.get_combined_dir(TMP_DIR, file_name)
        self.path_service.save_tmp_file(tmp_file_path, file_obj)
        if not self.upload_service.is_file_valid(file_type, upload_type, tmp_file_path):
            return Response("Invalid file uploaded", status=status.HTTP_400_BAD_REQUEST)

        # async
        user_dir = self.path_service.get_combined_dir(DATA_DIR, request.user.username)
        self.path_service.create_dir(user_dir)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset_name)
        if self.path_service.create_dir(dataset_dir, True):
            self.upload_service.save_file_data(tmp_file_path, dataset_dir, dataset_name, upload_type, request.user)
        self.path_service.delete_tmp_file(tmp_file_path)

        return Response(status=status.HTTP_204_NO_CONTENT)
