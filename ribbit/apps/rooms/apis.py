from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from serializers import RoomSerializer
from models import Room

class RoomViewSet(ViewSet):
    """
    The ViewSet of Room model
    """
    def list(self, request, format=None):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, format=None):
        rooms = Room.objects.all()
        room = get_object_or_404(rooms, pk=pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)