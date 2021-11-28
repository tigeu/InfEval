import base64

from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework import viewsets, permissions

from ObjectDetectionAnalyzer.main.serializers import UserSerializer, GroupSerializer, HeartbeatSerializer, \
    ImageSerializer
from ObjectDetectionAnalyzer.settings import DATA_DIR


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


def heartbeat(request, count):
    """
    Take incoming number and increment it.
    """
    count += 1
    response_data = {'count': count}
    serializer = HeartbeatSerializer(response_data)
    if request.method == 'GET':
        return JsonResponse(serializer.data, status=201)


def image(request, image_name):
    """
    Send image.
    """

    with open(DATA_DIR / image_name, mode='rb') as file:
        image_base64 = base64.b64encode(file.read()).decode('utf-8')

    response_data = {
        'name': image_name,
        'file': image_base64
    }

    serializer = ImageSerializer(response_data)

    if request.method == 'GET':
        return JsonResponse(serializer.data, status=201)
