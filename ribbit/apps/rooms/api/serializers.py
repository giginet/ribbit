from rest_framework import serializers
from ribbit.apps.users.api.serializers import UserSerializer
from ribbit.apps.rooms.models import Room

class RoomSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    members = UserSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'title', 'slug', 'description', 'scope', 'members', 'url')
