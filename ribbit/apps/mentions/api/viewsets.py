from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from serializers import MentionSerializer
from ..models import Mention
from permissions import IsOwn

class MentionViewSet(ViewSet):
    """
    The ViewSet of Mention model
    """

    permission_classes = [IsAuthenticated]

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

    @action(methods=['POST',], permission_classes=[IsOwn],)
    def mark_read(self, request, pk=None):
        mentions = Mention.objects.all()
        mention = get_object_or_404(mentions, pk=pk)
        if not mention.is_read:
            if mention.user == request.user:
                mention.is_read = True
                mention.save()
                return Response(status=200, data={'detail' : 'Mention %d was read' % mention.pk})
            return Response(status=403, data={'detail' : 'Permission Denied'})
