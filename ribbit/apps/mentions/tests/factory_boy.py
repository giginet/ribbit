import factory
from ribbit.apps.messages.tests.factory_boy import MessageFactory
from ribbit.apps.users.tests.factory_boy import UserFactory
from ..models import Mention

class MentionFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Mention

    user = factory.SubFactory(UserFactory)
    message = factory.SubFactory(MessageFactory)