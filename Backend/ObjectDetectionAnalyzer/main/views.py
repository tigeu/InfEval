from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class Heartbeat(APIView):
    """
    Handle requests sent to /heartbeat
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, count):
        """
        Take incoming number and increment it.
        """
        count += 1

        response_data = {'count': count}

        serializer = HeartbeatSerializer(response_data)

        return Response(serializer.data, status=status.HTTP_200_OK)
