from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from .models import Flatmate
from .serializers import FlatmateSerializer
import os
import shutil

# Create your views here.
class RegisterFlatmate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = FlatmateSerializer(data=request.data)
        if serializer.is_valid():
            flatmate = serializer.save()

            # Also save a copy of the image in /ai/known_faces/ as jpg
            src_path = flatmate.image.path
            dst_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ai', 'known_faces')
            dst_path = os.path.join(dst_dir, f"{flatmate.name}.jpg")
            shutil.copy(src_path, dst_path)

            return Response({"message": "Flatmate registered"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListFlatmates(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Flatmate.objects.all()
    serializer_class = FlatmateSerializer

class DeleteFlatmate(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            flatmate = Flatmate.objects.get(pk=pk)

            # Delete the known face image as well
            known_face_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ai', 'known_faces', f"{flatmate.name}.jpg")
            if os.path.exists(known_face_path):
                os.remove(known_face_path)

            flatmate.image.delete()
            flatmate.delete()
            return Response({"message": "Flatmate deleted"}, status=204)
        except Flatmate.DoesNotExist:
            return Response({"error": "Flatmate not found"}, status=404)