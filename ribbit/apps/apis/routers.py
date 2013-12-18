from rest_framework import routers
from django.conf.urls import patterns, include, url

from ribbit.apps.rooms.apis import RoomViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'rooms', RoomViewSet, base_name='room')

urlpatterns = router.urls
