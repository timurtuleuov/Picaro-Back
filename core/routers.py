from rest_framework_nested import routers

from core.post.viewsets import PostViewSet
from core.user.viewsets import UserViewSet
from core.auth.viewsets import RegisterViewSet, LoginViewSet, RefreshViewSet
from core.comment.viewsets import CommentViewSet
from django.urls import path
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
    path('user/<slug:slug>/', UserViewSet.as_view({'get': 'get_user_posts'}), name='user-posts'),
]