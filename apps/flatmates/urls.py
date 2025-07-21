from django.urls import path
from apps.flatmates.views import RegisterFlatmate, ListFlatmates, DeleteFlatmate

urlpatterns = [
    path("register/", RegisterFlatmate.as_view(), name="register_flatmate"),
    path("list/", ListFlatmates.as_view(), name="list_flatmates"),
    path("delete/<int:pk>/", DeleteFlatmate.as_view(), name="delete_flatmate"),
]