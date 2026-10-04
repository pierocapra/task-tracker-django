from django.urls import path
from . import views
from .views import health
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer

urlpatterns = [
    path('tasks', views.task_list),
    path('tasks/<int:pk>', views.task_detail),
    path("login", TokenObtainPairView.as_view(serializer_class=EmailTokenObtainPairSerializer)),
    path("health", health),
]