from django.db import models
from model_utils.models import TimeStampedModel


class Post(TimeStampedModel):
    user = models.ForeignKey("users.User", related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    body = models.TextField()

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey("users.User", related_name="likes", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
