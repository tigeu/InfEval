from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from ObjectDetectionAnalyzer.main.views.HeartbeatView import Heartbeat
from ObjectDetectionAnalyzer.main.views.ImageFilesView import ImageFiles
from ObjectDetectionAnalyzer.main.views.ImageView import Image
from ObjectDetectionAnalyzer.main.views.RegisterView import Register

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('heartbeat/<int:count>', Heartbeat.as_view(), name="heartbeat"),
    path('image/<str:image_name>', Image.as_view(), name="image"),
    path('image-files/', ImageFiles.as_view(), name="image-files"),
    path('register/', Register.as_view(), name="register"),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
