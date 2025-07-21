from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.core.files.storage import default_storage
from django.conf import settings
from apps.recognition.utils import verify_face_and_return_match
from apps.alerts.models import Alert
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
import shutil

# Define the known faces directory - fix the path
KNOWN_FACES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ai', 'known_faces')  

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

