from core.abstract.serializers import AbstractSerializer
from core.user.models import Friend_Resquest, User
from rest_framework import serializers

class UserSerializer(AbstractSerializer):
    class Meta:
        model = User
        # List of all the fields that can be included in a request or a response
        fields = ['id', 'slug', 'username', 'first_name', 'last_name', 'bio', 'avatar', 'friends', 'email', 'is_active',
                  'created', 'updated']
        # List of all the fields that can only be read by the user
        read_only_field = ['is_active']

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    to_user = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    class Meta:
        model = Friend_Resquest
        fields = ['id', 'from_user', 'to_user']