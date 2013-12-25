from django.test import TestCase

from ribbit.apps.users.tests.factory_boy import UserFactory
from ribbit.apps.rooms.tests.factory_boy import RoomFactory

from ribbit.apps.messages.models import Message
from ribbit.apps.messages.tests.factory_boy import MessageFactory

class MessageTestCase(TestCase):
    def setUp(self):
        pass

    def test_can_create_message(self):
        """Tests Message model returns correct attributes"""
        author = UserFactory(screen_name='renge')
        room = RoomFactory.create(slug='room')
        message = MessageFactory.create(body='nyanpass-', author=author, room=room)
        self.assertEqual(message.body, 'nyanpass-', 'body can be returned')
        self.assertEqual(message.author, author, 'author can be returned')
        self.assertEqual(message.room, room, 'room can be returned')

    def test_unicode(self):
        """Test __unicode__() returns correct value"""
        message = MessageFactory.create(body='toxuttoxuru-',
                                        author=UserFactory.create(screen_name='mayuri'),
                                        room=RoomFactory.create(title='lab chat'))
        self.assertEqual(unicode(message), 'toxuttoxuru- (mayuri) at lab chat', '__unicode__() returns correct value')

    def test_ordering(self):
        """Test messages are ordered in descending order by created_at"""
        user = UserFactory.create()
        message0 = MessageFactory.create(body='old message')
        message1 = MessageFactory.create(body='new message')
        qs = Message.objects.all()
        self.assertEqual(qs[0].body, 'new message')
        self.assertEqual(qs[1].body, 'old message')

    def test_meta_class(self):
        """Test meta class attributes is correct"""
        self.assertEqual(Message._meta.verbose_name.title(), 'Message', 'Meta.verbose_name is correct')
        self.assertEqual(Message._meta.verbose_name_plural.title(), 'Messages', 'Meta.verbose_name_plural is correct')

class MessageManagerTestCase(TestCase):
    def test_get_recent_messages(self):
        """Test get_recent_messages() returns messages correctly"""
        room0 = RoomFactory.create(slug='test-room')
        room1 = RoomFactory.create(slug='test-room2')
        for i in xrange(5):
            m = MessageFactory.create(room=room0, body='spam')
        for i in xrange(3):
            m = MessageFactory.create(room=room1, body='ham')
        qs0 = Message.objects.get_recent_messages(room0)
        qs1 = Message.objects.get_recent_messages(room1)
        self.assertEqual(len(qs0), 5)
        self.assertEqual(qs0[0].body, 'spam')
        self.assertEqual(len(qs1), 3)
        self.assertEqual(qs1[0].body, 'ham')

    def test_get_recent_messages_since(self):
        """Test get_recent_messages() returns messages correctly with since"""
        room = RoomFactory.create()
        for i in xrange(5):
            m = MessageFactory.create(room=room)
        qs = Message.objects.get_recent_messages(room)
        self.assertEqual(len(qs), 5)
        since = qs[2]
        self.assertEqual(len(Message.objects.get_recent_messages(room, since=since)), 2)

    def test_get_recent_messages_count(self):
        """Test get_recent_messages() returns messages correctly with count"""
        room = RoomFactory.create(slug='test-room')
        for i in xrange(5):
            m = MessageFactory.create(room=room)
        qs = Message.objects.get_recent_messages(room, count=3)
        self.assertEqual(len(qs), 3)
