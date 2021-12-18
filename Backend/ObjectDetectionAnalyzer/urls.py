from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from ObjectDetectionAnalyzer.image.views import Image
from ObjectDetectionAnalyzer.imagefiles.views import ImageFiles
from ObjectDetectionAnalyzer.main.views import Heartbeat
from ObjectDetectionAnalyzer.register.views import Register
from ObjectDetectionAnalyzer.upload.views import Upload

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('heartbeat/<int:count>', Heartbeat.as_view(), name="heartbeat"),
    path('image/<str:image_name>', Image.as_view(), name="image"),
    path('image-files/', ImageFiles.as_view(), name="image-files"),
    path('upload/<str:file_name>', Upload.as_view(), name="upload"),
    path('register/', Register.as_view(), name="register"),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
