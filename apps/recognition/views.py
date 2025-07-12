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
from apps.alerts.models import Alert
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
import shutil

# Define the known faces directory - fix the path
KNOWN_FACES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ai', 'known_faces')

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


class RecognizeFace(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        image=request.FILES.get("image")

        if not image:
            return Response({"error": "Image is required"}, status=400)

        # Save temp image OUTSIDE known_faces directory
        temp_path = os.path.join(settings.BASE_DIR, "temp.jpg")
        with open(temp_path, "wb+") as f:
            for chunk in image.chunks():
                f.write(chunk)

        matches = verify_face_and_return_match(temp_path)
        
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

        if matches:
            name, distance = matches[0]
            return Response({
                "match": name,
                "confidence": round(1 - distance, 3),
                "distance": round(distance, 4)
            }, status=200)
        else:
            Alert.objects.create(name="Unknown", image="UnknownFaceDetected.jpg")

            # Send Email Notification
            send_mail(
                subject="🚨 FlatGuard Alert: Unknown Face Detected",
                message=f"""
An unknown person was detected at your flat.

🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📍 Please check your alert logs or CCTV stream.
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['vc9958454536@gmail.com'],  # Replace with your email
                fail_silently=False,
            )

            return Response({"match": "Unknown"}, status=200)

