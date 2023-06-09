from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.post.serializers import PostSerializer
from core.user.serializers import UserSerializer
from core.user.models import User


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
        return Response(serializer.data)
