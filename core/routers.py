from rest_framework_nested import routers
from rest_framework import permissions
from core.post.viewsets import PostViewSet
from core.user.viewsets import UserViewSet
from core.auth.viewsets import RegisterViewSet, LoginViewSet, RefreshViewSet
from core.comment.viewsets import CommentViewSet
from core.user import viewsets
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import path


schema_view = get_schema_view(
    openapi.Info(
        title="Picaro API",
        default_version="v1",
        description="Swagger API for Picaro",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.SimpleRouter()

# ##################################################################### #
# ################### AUTH                       ###################### #
# ##################################################################### #

router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename='auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')


# ##################################################################### #
# ################### USER                       ###################### #
# ##################################################################### #

router.register(r'user', UserViewSet, basename='user')

# ##################################################################### #
# ################### POST                       ###################### #
# ##################################################################### #

router.register(r'post', PostViewSet, basename='post')

posts_router = routers.NestedSimpleRouter(router, r'post', lookup='post')
posts_router.register(r'comment', CommentViewSet, basename='post-comment')


urlpatterns = [
    *router.urls,
    *posts_router.urls,
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('user/<slug:pk>/posts/', UserViewSet.as_view({'get': 'get_user_posts'}), name='user-posts'),
    path('user/by_slug/<slug:slug>/', UserViewSet.as_view({'get': 'get_user_info'}), name='user-info'),
]