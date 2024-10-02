# serializers.py
from rest_framework import serializers
from .models import laptops

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = laptops
        fields = ['laptop_id', 'Brand']  # List the fields you want to include
