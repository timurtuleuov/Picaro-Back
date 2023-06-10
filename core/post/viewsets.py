from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post, PostImageMapping
from core.post.serializers import PostSerializer, PostImageMappingSerializer
from core.auth.permissions import UserPermission
from core.user.models import User

class PostViewSet(AbstractViewSet):
    http_method_names = ('post', 'get', 'put', 'delete')
    permission_classes = (UserPermission,)
    serializer_class = PostSerializer
    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        post_ids = [post.public_id for post in queryset]  # Список идентификаторов постов
        
        cover = PostImageMapping.objects.filter(post_uuid=queryset.values_list('public_id', flat=True)) # Используем post_id__in для фильтрации
        print("ЭТО КОВЕР")
        print("ЭТО КОВЕР", cover)
        print("ЭТО КОВЕР СВЕРХУ")
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Добавить связанные изображения в каждый объект поста
        for post_data in data:
            post_id = post_data['id']
            
            post_covers = PostImageMapping.objects.filter(post_uuid_in=post_id.all())  # Фильтруем изображения для текущего поста
            print(post_covers)
            post_data['cover'] = PostImageMappingSerializer(post_covers, many=True).data
            print(post_data['cover'])

        print("здесь ошибка 4")

        return Response(data)



    
    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Сохранение объектов PostImageMapping
        post = serializer.instance  # Получаем созданный объект Post
        cover_images = request.data.getlist('cover')  # Получаем список изображений

        for image in cover_images:
            PostImageMapping.objects.create(post_uuid=post.public_id, post_id=post.id, image=image)
        # Возвращаем данные сериализатора
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user

        user.like(post)

        serializer = self.serializer_class(post)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def remove_like(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user

        user.remove_like(post)

        serializer = self.serializer_class(post)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
