from core.abstract.serializers import AbstractSerializer
from core.user.models import User, Friend
from rest_framework import serializers

class UserSerializer(AbstractSerializer):
    class Meta:
        model = User
        # List of all the fields that can be included in a request or a response
        fields = ['id', 'slug', 'username', 'first_name', 'last_name', 'bio', 'avatar', 'friends', 'email', 'is_active',
                  'created', 'updated']
        # List of all the fields that can only be read by the user
        read_only_field = ['is_active']

class FriendSerializer(serializers.ModelSerializer):
    model = Friend
    created = serializers.DateTimeField(read_only=True)
    fields = ['id', 'friend_id', 'created']