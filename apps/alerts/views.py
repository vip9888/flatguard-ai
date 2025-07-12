from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Alert
from .serializer import AlertSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes

class AlertView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        alerts=Alert.objects.all().order_by('-timestamp')
        serializer=AlertSerializer(alerts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AlertCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer=AlertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

