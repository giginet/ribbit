import json
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from serializers import MessageSerializer
from rest_framework import permissions
from ribbit.apps.rooms.models import Room
from models import Message

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
