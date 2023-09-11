from django.db import models
from user_app.models import UserData
#model 
class Spam(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    marked_by = models.ManyToManyField(UserData)
    timestamp = models.DateTimeField(auto_now_add=True)
    spam_count = models.PositiveIntegerField(default=1)  # Default value is 1