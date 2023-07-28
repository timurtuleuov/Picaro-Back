from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from core.abstract.viewsets import AbstractViewSet
from core.comment.models import Comment
from core.comment.serializers import CommentSerializer
from core.post.models import Post, PostImageMapping
from core.post.serializers import PostImageMappingSerializer, PostSerializer
from core.user.serializers import FriendRequestSerializer, UserSerializer
from core.user.models import Friend_Resquest, User

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
    

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def create_friend_request(self, request, *args, **kwargs):
        user_from = self.request.user  # Пользователь, отправляющий заявку
        user_to = self.get_object()  # Пользователь, которому отправляется заявка

        if user_from == user_to:
            return Response({"detail": "Вы не можете отправить заявку на дружбу самому себе."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, существует ли уже заявка на дружбу между пользователями
        if Friend_Resquest.objects.filter(from_user=user_from, to_user=user_to).exists():
            return Response({"detail": "Заявка на дружбу уже существует."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем объект заявки на дружбу
        friend_request_data = {"from_user": user_from.id, "to_user": user_to.id}
        serializer = FriendRequestSerializer(data=friend_request_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #TODO сделать добавление друзей, это должно добавлять друга в поле friends таблицы User
    def accept_friend_request(self, request, *args, **kwargs):
        pass

    #TODO сделать отправку запросов, это должно добавляться в таблицу Friendship
