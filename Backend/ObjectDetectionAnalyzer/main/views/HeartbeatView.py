from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.main.serializers.HeartbeatSerializer import HeartbeatSerializer


class Heartbeat(APIView):
    """
    Handle requests sent to /heartbeat
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, count):
        """
        Take incoming number and increment it.
        """
        count += 1

        if request.user:
            print(request.user)
        else:
            print("Not authenticated")

        response_data = {'count': count}

        serializer = HeartbeatSerializer(response_data)

        return Response(serializer.data, status=status.HTTP_200_OK)
