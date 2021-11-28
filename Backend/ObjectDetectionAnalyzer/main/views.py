import base64
import os

from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework import viewsets, permissions

from ObjectDetectionAnalyzer.main.serializers import UserSerializer, GroupSerializer, HeartbeatSerializer, \
    ImageSerializer, FileSerializer
from ObjectDetectionAnalyzer.settings import DATA_DIR, IMAGE_ENDINGS


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


def image_files(request):
    all_file_names = os.listdir(DATA_DIR)
    image_names = []
    for file_name in all_file_names:
        base_name = os.path.basename(file_name)
        extension = os.path.splitext(file_name)[1]
        if extension.lower() in IMAGE_ENDINGS:
            image_names.append(base_name)

    response_data = [
        {'name': image_name} for image_name in image_names
    ]

    serializer = FileSerializer(response_data, many=True)

    if request.method == 'GET':
        return JsonResponse(serializer.data, status=201, safe=False)  # TODO how to do without making it "unsafe"
