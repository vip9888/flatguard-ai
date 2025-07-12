from django.urls import path
from . import views
from .views import GenAIChatView

urlpatterns = [
    path('chat/', GenAIChatView.as_view(), name='genai-chat'),
] 