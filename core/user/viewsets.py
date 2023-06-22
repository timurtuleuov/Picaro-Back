from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from core.abstract.viewsets import AbstractViewSet
from core.comment.models import Comment
from core.comment.serializers import CommentSerializer
from core.post.models import Post, PostImageMapping
from core.post.serializers import PostImageMappingSerializer, PostSerializer
from core.user.serializers import UserSerializer
from core.user.models import User

from django.shortcuts import get_object_or_404
from rest_framework import status


class UserViewSet(AbstractViewSet):
    http_method_names = ('patch', 'get')
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    
    @action(detail=True, methods=['get'], permission_classes=[]) 
    def get_user_posts(self, request, *args, **kwargs):
        user = User.objects.get_object_by_public_id(self.kwargs['pk'])
        posts = Post.objects.filter(author=user)
        serializer = PostSerializer(posts, many=True)
        data = serializer.data

        # Добавить связанные изображения и комментарии в каждый объект поста
        for post_data in data:
            post_id = post_data['id']
            # Получить изображения для текущего поста
            post_covers = PostImageMapping.objects.filter(post_uuid=post_id)
            cover_serializer = PostImageMappingSerializer(post_covers, many=True)
            post_data['cover'] = cover_serializer.data

            # Получить комментарии для текущего поста
            comments = Comment.objects.filter(post_uuid=post_id)
            comment_serializer = CommentSerializer(comments, many=True)
            post_data['comment'] = comment_serializer.data

        return Response(data)
    def get_user_info(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        user = get_object_or_404(User, slug=slug)
        serializer = self.serializer_class(user)
        

        return Response(data=serializer.data, status=status.HTTP_200_OK)