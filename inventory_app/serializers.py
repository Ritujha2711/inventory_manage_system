# serializers.py
from rest_framework import serializers
from .models import Item_details

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item_details
        fields = '__all__'
