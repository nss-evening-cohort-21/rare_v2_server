from django.db import models
from .post import Post
from .rare_user import RareUser

class Comment(models.Model):

    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_id = models.ForeignKey(RareUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_on = models.DateField()
