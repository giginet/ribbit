import factory
from models import Message

from ribbit.apps.users.factory_boy import UserFactory
from ribbit.apps.rooms.factory_boy import RoomFactory

class MessageFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Message

    room = factory.SubFactory(RoomFactory)
    author = factory.SubFactory(UserFactory)
