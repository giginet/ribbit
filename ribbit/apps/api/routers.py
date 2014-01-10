from rest_framework import routers

from ribbit.apps.users.api.viewsets import UserViewSet
from ribbit.apps.rooms.api.viewsets import RoomViewSet
from ribbit.apps.messages.api.viewsets import MessageViewSet
from ribbit.apps.mentions.api.viewsets import MentionViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'rooms', RoomViewSet, base_name='room')
router.register(r'users', UserViewSet, base_name='user')
router.register(r'messages', MessageViewSet, base_name='message')
router.register(r'mentions', MentionViewSet, base_name='mention')

urlpatterns = router.urls
