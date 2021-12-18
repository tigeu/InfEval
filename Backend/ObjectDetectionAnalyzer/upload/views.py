from pathlib import Path

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.settings import DATA_DIR


class Upload(APIView):
    """
    Handle requests sent to /register
    """
    parser_classes = [MultiPartParser]

    def put(self, request, file_name):
        file_obj = request.data['file']

        user_dir = DATA_DIR / request.user.username
        Path(user_dir).mkdir(parents=True, exist_ok=True)

        with open(user_dir / file_name, "wb") as file:
            file.write(file_obj.read())

        return Response(status=status.HTTP_204_NO_CONTENT)
