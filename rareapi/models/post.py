from django.db import models
from .category import Category
from .rare_user import RareUser


class Post(models.Model):

    rare_user_id = models.ForeignKey(RareUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=500)
    approved = models.BooleanField(default=False)
