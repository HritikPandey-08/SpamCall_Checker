from rest_framework import serializers
from .models import UserData

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id', 'name', 'phone_number', 'email_address', 'password']
        # extra_kwargs = {'password': {'write_only': True}}
