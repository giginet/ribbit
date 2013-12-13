import factory
from models import User

class UserFactory(factory.Factory):
    FACTORY_FOR = User

    username = 'kawaztan'
    email = 'webmaster@kawaz.org'
