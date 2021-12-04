from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from ObjectDetectionAnalyzer.main.views.AuthenticationView import UserViewSet, GroupViewSet
from ObjectDetectionAnalyzer.main.views.HeartbeatView import Heartbeat
from ObjectDetectionAnalyzer.main.views.ImageFilesView import ImageFiles
from ObjectDetectionAnalyzer.main.views.ImageView import Image

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('heartbeat/<int:count>', Heartbeat.as_view()),
    path('image/<str:image_name>', Image.as_view()),
    path('image-files', ImageFiles.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
