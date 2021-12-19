from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from ObjectDetectionAnalyzer.image.ImageView import ImageView
from ObjectDetectionAnalyzer.imagefiles.ImageFilesView import ImageFilesView
from ObjectDetectionAnalyzer.main.HeartbeatView import HeartbeatView
from ObjectDetectionAnalyzer.register.RegisterView import RegisterView
from ObjectDetectionAnalyzer.upload.UploadView import UploadView

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('heartbeat/<int:count>', HeartbeatView.as_view(), name="heartbeat"),
    path('image/<str:image_name>', ImageView.as_view(), name="image"),
    path('image-files/', ImageFilesView.as_view(), name="image-files"),
    path('upload/<str:file_name>', UploadView.as_view(), name="upload"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
