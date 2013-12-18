from serializers import RoomSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from models import Room

class RoomViewSet(ViewSet):
    """
    The ViewSet of Room model
    """
    def list(self, request, format=None):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)