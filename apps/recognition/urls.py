from django.urls import path
from apps.recognition.views import RecognizeFace

urlpatterns = [
    path("recognize/", RecognizeFace.as_view(), name="recognize_face"),

]