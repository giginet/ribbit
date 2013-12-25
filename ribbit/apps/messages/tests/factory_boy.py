import factory
from ..models import Message

from ribbit.apps.users.tests.factory_boy import UserFactory
from ribbit.apps.rooms.tests.factory_boy import RoomFactory

class MessageFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Message

    room = factory.SubFactory(RoomFactory)
    author = factory.SubFactory(UserFactory)
