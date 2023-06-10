from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core.abstract.serializers import AbstractSerializer
from core.post.models import Post, PostImageMapping
from core.user.models import User
from core.user.serializers import UserSerializer


class PostImageMappingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = PostImageMapping
        fields = ['id', 'image', 'post_id']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        cover = PostImageMapping.objects.filter(post_id__in=queryset)
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Добавить связанные изображения в каждый объект поста с порядковыми id
        for post_data in data:
            post_id = post_data['__id']
            post_data['cover'] = PostImageMappingSerializer(cover.filter(post_id=post_id), many=True).data

        return Response(data)


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='public_id')
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    cover = PostImageMappingSerializer(source='images', many=True, read_only=True)

    def get_liked(self, instance):
        request = self.context.get('request', None)
        if request is None or request.user.is_anonymous:
            return False
        return request.user.has_liked(instance)

    def get_likes_count(self, instance):
        return instance.liked_by.count()

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't create a post for another user.")
        return value

    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep["author"])
        rep["author"] = UserSerializer(author).data
        return rep

    class Meta:
        model = Post
        fields = ['id', 'author', 'body', 'cover', 'edited', 'liked', 'likes_count', 'created', 'updated']
        read_only_fields = ["edited"]
