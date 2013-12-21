from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from ribbit.apps.messages.api.serializers import MessageSerializer
from ribbit.apps.rooms.models import Room
from ribbit.apps.messages.models import Message

class MessageViewSet(ViewSet):
    """
    The ViewSet of Message model
    """
    def list(self, request, format):
        room_slug = request.GET.get('room', '')
        try:
            room = Room.objects.get(slug=room_slug)
            qs = Message.objects.filter(room=room)
            serializer = MessageSerializer(qs, many=True)
            return Response(serializer.data)
        except:
            return Response(status=404, data={'status': 'error', 'message' : 'Room ID is invalid'})
