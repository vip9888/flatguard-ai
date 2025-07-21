from rest_framework import serializers
from .models import Flatmate

class FlatmateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flatmate
        fields = ['id', 'name', 'image']