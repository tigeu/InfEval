from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.register.UserSerializer import UserSerializer


class RegisterView(APIView):
    """
    Handle requests sent to /register
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.initial_data['username']
            email = serializer.initial_data['email']
            password = serializer.initial_data['password']
            User.objects.create_user(username, email, password)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
