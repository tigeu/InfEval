from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView


class Upload(APIView):
    """
    Handle requests sent to /register
    """
    parser_classes = [MultiPartParser]

    def put(self, request, file_name):
        file_obj = request.data['file']
        with open(file_name, "wb") as file:
            file.write(file_obj.read())

        return Response(status=status.HTTP_204_NO_CONTENT)
