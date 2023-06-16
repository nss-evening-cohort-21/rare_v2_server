from django.db import models
from .category import Category

class RareUser(models.Model):

    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    category = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateField()
    header_image_url = models.ForeignKey(User, on_delete=models.CASCADE)
