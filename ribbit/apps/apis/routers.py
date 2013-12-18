from rest_framework import routers

from ribbit.apps.users.apis import UserViewSet
from ribbit.apps.rooms.apis import RoomViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'rooms', RoomViewSet, base_name='room')
router.register(r'users', UserViewSet, base_name='user')

urlpatterns = router.urls
