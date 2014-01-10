from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from serializers import MentionSerializer
from ..models import Mention

class MentionViewSet(ViewSet):
    """
    The ViewSet of Mention model
    """
    def list(self, request, format=None):
        user = request.GET.get('user', '')
        room = request.GET.get('room', '')
        query = {}
        if user: query['user__username'] = user
        if room: query['message__room__slug'] = room
        mentions = Mention.objects.filter(**query)
        serializer = MentionSerializer(mentions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, format=None):
        mentions = Mention.objects.all()
        mention = get_object_or_404(mentions, pk=pk)
        serializer = MentionSerializer(mention)
        return Response(serializer.data)