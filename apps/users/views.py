from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
# For JWT login and refresh
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes

class RegisterView(generics.CreateAPIView):
    permission_classed = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

