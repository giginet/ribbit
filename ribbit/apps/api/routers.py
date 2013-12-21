from rest_framework import routers

from ribbit.apps.users.api.api import UserViewSet
from ribbit.apps.rooms.api.views import RoomViewSet
from ribbit.apps.messages.api.views import MessageViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'rooms', RoomViewSet, base_name='room')
router.register(r'users', UserViewSet, base_name='user')
router.register(r'messages', MessageViewSet, base_name='message')

urlpatterns = router.urls
