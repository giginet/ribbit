from rest_framework import serializers
from ribbit.apps.messages.api.serializers import MessageSerializer
from ribbit.apps.rooms.api.serializers import RoomSerializer
from ..models import Mention

class MentionSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    message = MessageSerializer()
    in_reply_to = MessageSerializer()

    class Meta:
        model = Mention
        fields = ('id', 'message', 'user', 'in_reply_to', 'is_read')
