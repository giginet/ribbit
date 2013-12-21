import factory
from models import Room, Role

from ribbit.apps.users.factory_boy import UserFactory

class RoleFactory(factory.Factory):
    FACTORY_FOR = Role

class RoomFactory(factory.Factory):
    FACTORY_FOR = Room

    title = 'Test Chat'
    slug = 'test-chat'
    author = factory.SubFactory(UserFactory)