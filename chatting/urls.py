from django.urls import path
from .views import ChatbotAPIView, ChatDetailAPIView

urlpatterns = [
    path('', ChatbotAPIView.as_view(), name='chat'),
    path('<int:pk>/', ChatDetailAPIView.as_view(), name='chat_detail')
    
]
