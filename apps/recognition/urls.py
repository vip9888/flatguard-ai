from django.urls import path
from apps.recognition.views import RegisterFlatmate, RecognizeFace, ListFlatmates, DeleteFlatmate

urlpatterns = [
    path("register/", RegisterFlatmate.as_view(), name="register_flatmate"),
    path("recognize/", RecognizeFace.as_view(), name="recognize_face"),
    path("list/", ListFlatmates.as_view(), name="list_flatmates"),
    path("delete/<int:pk>/", DeleteFlatmate.as_view(), name="delete_flatmate"),
]