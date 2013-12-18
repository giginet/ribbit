from rest_framework import serializers
from ribbit.apps.users.serializers import UserSerializer
from models import Room

class RoomSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    members = UserSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'title', 'slug', 'description', 'scope', 'members', 'created_at', 'updated_at', 'url')
