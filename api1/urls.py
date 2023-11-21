from django.urls import path, include
from .views import SignUpAPIView, LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
]
