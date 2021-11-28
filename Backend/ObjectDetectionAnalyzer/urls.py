from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from ObjectDetectionAnalyzer.main import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('heartbeat/<int:count>', views.heartbeat),
    path('image/<str:image_name>', views.image),
    path('image-files', views.image_files),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
