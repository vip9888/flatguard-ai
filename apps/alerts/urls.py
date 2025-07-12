from django.urls import path
from . import views
from .views import AlertView

urlpatterns = [
    # Add alert-related URLs here when needed
    # For now, this is a placeholder
    path('alerts/', AlertView.as_view(), name='alerts'),
] 