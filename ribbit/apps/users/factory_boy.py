import factory
from models import User

class UserFactory(factory.Factory):
    FACTORY_FOR = User

    last_name = 'Inonaka'
    first_name = 'Kawaz'
    username = 'kawaztan'
    email = 'webmaster@kawaz.org'
    screen_name = 'Kawaz tan'
