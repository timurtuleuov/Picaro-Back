from django.db import models
from core.abstract.models import AbstractModel, AbstractManager

class PostManager(AbstractManager):
    pass

class Post(AbstractModel):
    author = models.ForeignKey(to="core_user.User", on_delete=models.CASCADE)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    images = models.ManyToManyField("PostImageMapping", related_name="posts")

    objects = PostManager()

    def __str__(self):
        return f"{self.author.name}"

class PostImageMapping(models.Model):
    image = models.ImageField(upload_to="covers/")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image_mappings')
    post_uuid = models.UUIDField()

    def __str__(self):
        return str(self.image)
