from rest_framework import routers

from ribbit.apps.users.apis import UserViewSet
from ribbit.apps.rooms.apis import RoomViewSet
from ribbit.apps.messages.apis import MessageViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'rooms', RoomViewSet, base_name='room')
router.register(r'users', UserViewSet, base_name='user')
router.register(r'messages', MessageViewSet, base_name='message')

urlpatterns = router.urls
