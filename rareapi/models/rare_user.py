from django.db import models
from .user import User


class RareUser(models.Model):

    bio = models.CharField(max_length=100)
    profile_image_url = models.CharField(max_length=500)
    created_on = models.DateField()
    active = models.BooleanField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
