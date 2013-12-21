from rest_framework import serializers
from ribbit.apps.users.serializers import UserSerializer
from ribbit.apps.rooms.serializers import RoomSerializer
from models import Message

class MessageSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    room = RoomSerializer()

    class Meta:
        model = Message
        fields = ('id', 'body', 'author', 'room', 'created_at', 'updated_at',)

