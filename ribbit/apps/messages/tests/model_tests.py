from django.test import TestCase

from ribbit.apps.users.factory_boy import UserFactory
from ribbit.apps.rooms.factory_boy import RoomFactory

from ribbit.apps.messages.models import Message
from ribbit.apps.messages.factory_boy import MessageFactory

class MessageTestCase(TestCase):
    def setUp(self):
        pass

    def test_can_create_message(self):
        """Tests Message model returns correct attributes"""
        message = MessageFactory.create(body=u'nyanpass-')
        author = UserFactory(screen_name='renge')
        room = MessageFactory.attributes()['room']
        self.assertEqual(message.body, 'nyanpass-', 'body can be returned')
        self.assertEqual(message.author, author, 'author can be returned')
        self.assertEqual(message.room, room, 'room can be returned')

    def test_unicode(self):
        """Test __unicode__() returns correct value"""
        message = MessageFactory.create(body='toxuttoxuru-',
                                        author=UserFactory.create(screen_name='mayuri'),
                                        room=RoomFactory.create(title='lab chat'))
        self.assertEqual(unicode(message), 'toxuttoxuru- (mayuri) at lab chat', '__unicode__() returns correct value')

    def test_meta_class(self):
        message = MessageFactory.build()
        self.assertEqual(Message._meta.verbose_name.title(), 'Message', 'Meta.verbose_name is correct')
        self.assertEqual(Message._meta.verbose_name_plural.title(), 'Messages', 'Meta.verbose_name_plural is correct')
