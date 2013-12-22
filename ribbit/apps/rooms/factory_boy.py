import factory
from models import Room, Role

from ribbit.apps.users.factory_boy import UserFactory

class RoleFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Role

class RoomFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Room
    FACTORY_DJANGO_GET_OR_CREATE = ('slug',)

    title = 'Test Chat'
    slug = factory.Sequence(lambda n: 'test-chat{0}'.format(n))
    author = factory.SubFactory(UserFactory)