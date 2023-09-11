from rest_framework import serializers
from .models import Spam

class SpamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spam
        fields = ['phone_number', 'spam_count','marked_by', 'timestamp']
