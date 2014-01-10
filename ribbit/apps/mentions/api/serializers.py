from rest_framework import serializers
from ribbit.apps.messages.api.serializers import MessageSerializer
from ribbit.apps.users.api.serializers import UserSerializer
from ..models import Mention

class MentionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    message = MessageSerializer()
    in_reply_to = MessageSerializer()

    class Meta:
        model = Mention
        fields = ('id', 'message', 'user', 'in_reply_to', 'is_read')
