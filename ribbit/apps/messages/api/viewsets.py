from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import link

from ribbit.apps.messages.api.serializers import MessageSerializer
from ribbit.apps.rooms.models import Room
from ribbit.apps.rooms.api.permissions import ViewPermission
from ribbit.apps.messages.models import Message

class MessageViewSet(ViewSet):
    """
    The ViewSet of Message model
    """

    permission_classes = [ViewPermission]

    def list(self, request, format=None):
        try:
            room_slug = request.GET.get('room', '')
            since = request.GET.get('since', None)
            count = request.GET.get('count', '100')
            room = Room.objects.get(slug=room_slug)
            kwargs = {
                'room' : room
            }
            if count.isdigit(): kwargs['count'] = int(count)
            if since:
                message = Message.objects.get(pk=since)
                kwargs['since'] = message
            qs = Message.objects.get_recent_messages(**kwargs)
            serializer = MessageSerializer(qs, many=True)
            return Response(serializer.data)
        except:
            return Response(status=404, data={'detail' : 'Room ID is invalid'})
