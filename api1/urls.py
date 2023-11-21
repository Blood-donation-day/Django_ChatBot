from django.urls import path, include
from .views import SignUpAPIView, LoginAPIView, ProfileAPIView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
]
