from rest_framework import serializers
from ribbit.apps.users.api.serializers import UserSerializer
from ribbit.apps.rooms.api.serializers import RoomSerializer
from ribbit.apps.messages.models import Message

class MessageSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    room = RoomSerializer()

    class Meta:
        model = Message
        fields = ('id', 'body', 'author', 'room', 'created_at', 'updated_at',)

