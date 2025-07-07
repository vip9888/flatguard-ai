from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.core.files.storage import default_storage
from django.conf import settings
from apps.recognition.utils import verify_face_and_return_match
from .models import Flatmate
from .serializers import FlatmateSerializer
import shutil

class RegisterFlatmate(APIView):
    def post(self, request):
        serializer = FlatmateSerializer(data=request.data)
        if serializer.is_valid():
            flatmate = serializer.save()

            # Also save a copy of the image in /ai/known_faces/ as jpg
            src_path = flatmate.image.path
            dst_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ai', 'known_faces')
            dst_path = os.path.join(dst_dir, f"{flatmate.name}.jpg")
            shutil.copy(src_path, dst_path)

            return Response({"message": "Flatmate registered"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListFlatmates(ListAPIView):
    queryset = Flatmate.objects.all()
    serializer_class = FlatmateSerializer

class DeleteFlatmate(APIView):
    def delete(self, request, pk):
        try:
            flatmate = Flatmate.objects.get(pk=pk)

            # Delete the known face image as well
            known_face_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ai', 'known_faces', f"{flatmate.name}.jpg")
            if os.path.exists(known_face_path):
                os.remove(known_face_path)

            flatmate.image.delete()
            flatmate.delete()
            return Response({"message": "Flatmate deleted"}, status=204)
        except Flatmate.DoesNotExist:
            return Response({"error": "Flatmate not found"}, status=404)



class RecognizeFace(APIView):
    def post(self,request):
        image=request.FILES.get("image")

        if not image:
            return Response({"error": "Image is required"}, status=400)

        temp_path = os.path.join(KNOWN_FACES_DIR, "temp.jpg")
        with open(temp_path, "wb+") as f:
            for chunk in image.chunks():
                f.write(chunk)

        matches = verify_face_and_return_match(temp_path)
        os.remove(temp_path)

        if matches:
            return Response({"match": matches[0][0]}, status=200)
        else:
            return Response({"match": "Unknown"}, status=200)

