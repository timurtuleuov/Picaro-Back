from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from autoslug import AutoSlugField
from CoreRoot import settings
from core.abstract.models import AbstractModel, AbstractManager
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save


class UserManager(BaseUserManager, AbstractManager):

    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a `User` with an email, phone number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')
        if password is None:
            raise TypeError('User must have an email.')

        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **kwargs):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class Friend(models.Model):
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    friend_id = models.UUIDField()
    created = models.DateTimeField(auto_now_add=True)

class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    slug = AutoSlugField(populate_from='username', unique=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    bio = models.TextField(null=True)
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default-avatar.png')
    friends = models.ManyToManyField(Friend)
    posts_liked = models.ManyToManyField(
        "core_post.Post",
        related_name="liked_by"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"


    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def like(self, post):
        """Like `post` if it hasn't been done yet"""
        return self.posts_liked.add(post)

    def remove_like(self, post):
        """Remove a like from a `post`"""
        return self.posts_liked.remove(post)

    def has_liked(self, post):
        """Return True if the user has liked a `post`; else False"""
        return self.posts_liked.filter(pk=post.pk).exists()

@receiver(pre_save, sender=User)
def generate_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.username)

# class Friendship(models.Model):
#     user = models.MAN
#     friend_uuid = models.UUIDField()

