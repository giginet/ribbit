import factory
from ..models import User

class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    last_name = 'Inonaka'
    first_name = 'Kawaz'
    username = factory.sequence(lambda n: 'kawaztan{0}'.format(n))
    email = 'webmaster@kawaz.org'
    screen_name = 'Kawaz tan'
    password = 'pass'
