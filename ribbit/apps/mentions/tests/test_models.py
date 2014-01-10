from django.test.testcases import TestCase
from ribbit.apps.users.tests.factory_boy import UserFactory
from ribbit.apps.messages.tests.factory_boy import MessageFactory
from ribbit.apps.rooms.tests.factory_boy import RoomFactory
from factory_boy import MentionFactory
from ..models import Mention

class MentionManagerTestCase(TestCase):
    def setUp(self):
        self.user0 = UserFactory.create(username='user0')
        self.user1 = UserFactory.create(username='user1')
        self.user2 = UserFactory.create(username='user2')

    def test_no_mention(self):
        """Test return empty QuerySet from message contains no mention"""
        message = MessageFactory.create(body='This is a not mention message. Hello!!!!')
        qs = Mention.objects.create_from_message(message)
        self.assertEqual(qs.count(), 0)

    def test_one_mention(self):
        """Test return QuerySet from message contains one mention"""
        message = MessageFactory.create(body='@user0 Hello, user0!!! This message mention to you.')
        qs = Mention.objects.create_from_message(message)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].user, self.user0)
        self.assertEqual(qs[0].message, message)
        self.assertFalse(qs[0].is_read)

    def test_mention_with_in_reply_to(self):
        """Test return QuerySet contains mention with in_reply_to"""
        message = MessageFactory.create(body='@user0 Hello, user0!!! This message mention to you.')
        reply_to = MessageFactory.create()
        qs = Mention.objects.create_from_message(message, reply_to)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].user, self.user0)
        self.assertEqual(qs[0].message, message)
        self.assertEqual(qs[0].in_reply_to, reply_to)
        self.assertFalse(qs[0].is_read)

    def test_two_mentions(self):
        """Test return QuerySet from message contains two mentions"""
        message = MessageFactory.create(body='@user0 @user1 Hello, user0, user1!!! This message mention to you.')
        qs = Mention.objects.create_from_message(message)
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs[0].user, self.user0)
        self.assertEqual(qs[0].message, message)
        self.assertFalse(qs[0].is_read)
        self.assertEqual(qs[1].user, self.user1)
        self.assertEqual(qs[1].message, message)
        self.assertFalse(qs[1].is_read)

    def test_not_exist_user_mention(self):
        """Test return empty QuerySet from message contains mention for not exist user"""
        message = MessageFactory.create(body='@empty_user Hello!!!!!!!!! Is there somebody?')
        qs = Mention.objects.create_from_message(message)
        self.assertEqual(qs.count(), 0)

    def test_mention_with_multiple_times(self):
        """Test return QuerySet from message contains mention for one user with multiple times"""
        message = MessageFactory.create(body='@user0 @user0 @user0 @user0 multiple mentions!!!')
        reply_to = MessageFactory.create()
        qs = Mention.objects.create_from_message(message, reply_to)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].user, self.user0)
        self.assertEqual(qs[0].message, message)
        self.assertEqual(qs[0].in_reply_to, reply_to)
        self.assertFalse(qs[0].is_read)

    def test_all_users_mention(self):
        """Test returns QuerySet from message contains mention for all"""
        room = RoomFactory.create(author=self.user0)
        room.add_member(self.user2)
        message = MessageFactory.create(body='@all Hello, every one. This is a broadcast message', room=room)
        qs = Mention.objects.create_from_message(message)
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs[0].user, self.user0)
        self.assertEqual(qs[0].message, message)
        self.assertFalse(qs[0].is_read)
        self.assertEqual(qs[1].user, self.user2)
        self.assertEqual(qs[1].message, message)
        self.assertFalse(qs[1].is_read)

    def test_all_users_mention_with_duplicated_user(self):
        """Test returns QuerySet from message contains mention for all and duplicated user."""
        room = RoomFactory.create(author=self.user0)
        room.add_member(self.user2)
        room.add_member(self.user0)
        message = MessageFactory.create(body='@all Hello, every one. This is a broadcast message. @user0 Hello, user0', room=room)
        qs = Mention.objects.create_from_message(message)
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs[0].user, self.user0)
        self.assertEqual(qs[0].message, message)
        self.assertFalse(qs[0].is_read)
        self.assertEqual(qs[1].user, self.user2)
        self.assertEqual(qs[1].message, message)
        self.assertFalse(qs[1].is_read)

    def test_all_users_mention_with_not_member_user(self):
        """Test returns QuerySet from message contains mention for all and not member user."""
        room = RoomFactory.create(author=self.user0)
        room.add_member(self.user0)
        room.add_member(self.user2)
        message = MessageFactory.create(body='@all Hello, every one. This is a broadcast message, @user1 Hello user1', room=room)
        qs = Mention.objects.create_from_message(message)
        self.assertEqual(qs.count(), 3)
        self.assertEqual(qs[0].user, self.user0)
        self.assertEqual(qs[0].message, message)
        self.assertFalse(qs[0].is_read)
        self.assertEqual(qs[1].user, self.user1)
        self.assertEqual(qs[1].message, message)
        self.assertFalse(qs[1].is_read)
        self.assertEqual(qs[2].user, self.user2)
        self.assertEqual(qs[2].message, message)
        self.assertFalse(qs[2].is_read)

class MentionModelTestCase(TestCase):
    def test_mention(self):
        """Test mention object can be created"""
        mention = MentionFactory.create()
        self.assertIsNotNone(mention.user)
        self.assertIsNotNone(mention.message)
        self.assertIsNone(mention.in_reply_to)
        self.assertFalse(mention.is_read)

    def test_unicode(self):
        """Test __unicode__() returns correct name"""
        mention = MentionFactory.create()
        self.assertEqual(unicode(mention), unicode(mention.message))

    def test_meta(self):
        """Test Meta class returns correct values"""
        self.assertEqual(Mention._meta.verbose_name.title(), 'Mention')
        self.assertEqual(Mention._meta.verbose_name_plural.title(), 'Mentions')

class MentionSignalTestCase(TestCase):
    def setUp(self):
        self.user0 = UserFactory.create(username='user0')
        self.user1 = UserFactory.create(username='user1')
        self.user2 = UserFactory.create(username='user2')

    def test_create_mention(self):
        """Test mention will be created when message was published"""
        message = MessageFactory.create(body=u'@user0 @user1 Hello!!!!!!!')
        self.assertIsNotNone(Mention.objects.get(message=message, user=self.user0))
        self.assertIsNotNone(Mention.objects.get(message=message, user=self.user1))

    def test_create_all_mention(self):
        """Test mentions will be created when message which contains @all was published"""
        room = RoomFactory.create(author=self.user0)
        room.add_member(self.user0)
        room.add_member(self.user2)
        message = MessageFactory.create(body='@all Hello, every one. This is a broadcast message', room=room)
        qs = Mention.objects.filter(message=message)
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs[0].user, self.user0)
        self.assertEqual(qs[0].message, message)
        self.assertFalse(qs[0].is_read)
        self.assertEqual(qs[1].user, self.user2)
        self.assertEqual(qs[1].message, message)
        self.assertFalse(qs[1].is_read)
