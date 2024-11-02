from rest_framework import serializers
from .models import Items

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'  # This includes all fields in the Items model

        # Alternatively, you can specify the fields explicitly:
        # fields = ['id', 'name', 'description']
