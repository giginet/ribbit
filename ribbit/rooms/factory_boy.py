import factory
from models import Room

from users.factory_boy import UserFactory

class RoomFactory(factory.Factory):
    FACTORY_FOR = Room

    title = 'Test Chat'
    slug = 'test-chat'
    author = factory.SubFactory(UserFactory)