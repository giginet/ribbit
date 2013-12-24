from django.test import TestCase
from django.core.urlresolvers import reverse

from ribbit.apps.users.factory_boy import UserFactory
from ribbit.apps.rooms.factory_boy import RoomFactory

from ribbit.apps.users.models import User
from ribbit.apps.messages.models import Message
from ribbit.apps.messages.factory_boy import MessageFactory

class UserTestCase(TestCase):
    def test_can_create_user(self):
        """Tests Message model returns correct attributes"""
        user = UserFactory.create(twitter='@kawaztan', screen_name='Kawaz tan', username='kawaztan')
        self.assertEqual(user.username, 'kawaztan', 'username can be returned')
        self.assertEqual(user.screen_name, 'Kawaz tan', 'screen_name can be returned')
        self.assertEqual(user.twitter, '@kawaztan', 'twitter can be returned')

    def test_unicode(self):
        """Test __unicode__() returns correct value"""
        message = UserFactory.create(username='kawaztan', screen_name='Kawaz tan')
        self.assertEqual(unicode(message), 'Kawaz tan(kawaztan)', '__unicode__() returns correct value')

    def test_get_absolute_url(self):
        """Test get_absolute_url() returns correct URL."""
        user = UserFactory.create()
        self.assertEqual(reverse('users_user_detail', args=(user.username,)), user.get_absolute_url())
        self.assertEqual('/users/%s/' % user.username, user.get_absolute_url())

    def test_meta_class(self):
        """Test meta class attributes is correct"""
        self.assertEqual(User._meta.verbose_name.title(), 'User', 'Meta.verbose_name is correct')
        self.assertEqual(User._meta.verbose_name_plural.title(), 'Users', 'Meta.verbose_name_plural is correct')

