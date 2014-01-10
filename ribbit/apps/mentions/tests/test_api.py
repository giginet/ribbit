import json
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from ribbit.apps.rooms.tests.factory_boy import RoomFactory
from ribbit.apps.users.tests.factory_boy import UserFactory
from ribbit.apps.messages.tests.factory_boy import MessageFactory
from ..models import Mention
from factory_boy import MentionFactory

class MentionListAPITestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.set_password('password')
        self.user.save()
        self.room0 = RoomFactory()
        self.room1 = RoomFactory()
        self.message0 = MessageFactory()
        self.message1 = MessageFactory()

    def test_not_authorized_user(self):
        """Test not authorized user cant access to the API"""
        c = Client()
        response = c.get(reverse('mention-list'))
        dict = json.loads(response.content)
        self.assertIsNotNone(dict.get('detail'))
        self.assertEqual(response.status_code, 403)

    def test_all_mentions_list(self):
        """Test authorized user can get all mentions list"""
        c = Client()
        mention = MentionFactory()
        self.assertTrue(c.login(username=self.user.username, password='password'))
        response = c.get(reverse('mention-list'))
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['id'], mention.pk)
        self.assertEqual(response_json[0]['user']['id'], mention.user.pk)
        self.assertEqual(response_json[0]['message']['id'], mention.message.pk)
        self.assertIsNone(response_json[0]['in_reply_to'])
        self.assertFalse(response_json[0]['is_read'])

    def test_mentions_list_with_room(self):
        """Test authorized user can get all mentions list"""
        c = Client()
        mention0 = MentionFactory(message=self.message0)
        mention1 = MentionFactory(message=self.message1)
        self.assertTrue(c.login(username=self.user.username, password='password'))

        response = c.get(reverse('mention-list'))
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)

        response = c.get(reverse('mention-list'), {'room' : self.message0.room.slug})
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['id'], mention0.pk)

        response = c.get(reverse('mention-list'), {'room' : self.message1.room.slug})
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['id'], mention1.pk)

    def test_mentions_list_with_user(self):
        """Test authorized user can get all mentions list"""
        c = Client()
        mention0 = MentionFactory(user=self.user)
        mention1 = MentionFactory()
        self.assertTrue(c.login(username=self.user.username, password='password'))

        response = c.get(reverse('mention-list'))
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)

        response = c.get(reverse('mention-list'), {'user' : self.user.username})
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['id'], mention0.pk)

        response = c.get(reverse('mention-list'), {'user' : mention1.user.username})
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['id'], mention1.pk)

class MentionMarkReadAPITestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.set_password('password')
        self.user.save()
        self.room0 = RoomFactory()
        self.room1 = RoomFactory()
        self.message0 = MessageFactory()
        self.message1 = MessageFactory()

    def test_not_authorized_user(self):
        """Test not authorized user cant access to the API"""
        c = Client()
        mention = MentionFactory()
        response = c.post(reverse('mention-mark-read', args=(mention.pk,)))
        dict = json.loads(response.content)
        self.assertIsNotNone(dict.get('detail'))
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        """Test user can't access mark-read using GET method"""
        mention = MentionFactory(user=self.user)
        c = Client()
        response = c.get(reverse('mention-mark-read', args=(mention.pk,)))
        self.assertEqual(response.status_code, 405)

    def test_mark_read(self):
        """Test user make own mention to mark read"""
        c = Client()
        mention = MentionFactory(user=self.user)
        self.assertTrue(c.login(username=self.user.username, password='password'))
        self.assertFalse(mention.is_read)
        response = c.post(reverse('mention-mark-read', args=(mention.pk,)))
        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'], 'Mention %d was read' % mention.pk)
        self.assertEqual(response.status_code, 200)
        mention = Mention.objects.get(pk=mention.pk)
        self.assertTrue(mention.is_read)

    def test_mark_read_with_not_owner(self):
        """Test user can't make other's mention to mark read"""
        c = Client()
        mention = MentionFactory()
        self.assertTrue(c.login(username=self.user.username, password='password'))
        self.assertFalse(mention.is_read)
        response = c.post(reverse('mention-mark-read', args=(mention.pk,)))
        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'], 'Permission Denied')
        self.assertEqual(response.status_code, 403)
        self.assertFalse(mention.is_read)

    def test_mark_read_with_invalid_mention(self):
        """Test user can't make other's mention to mark read"""
        c = Client()
        mention = MentionFactory(user=self.user)
        self.assertTrue(c.login(username=self.user.username, password='password'))
        self.assertFalse(mention.is_read)
        response = c.post(reverse('mention-mark-read', args=(-1,)))
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(mention.is_read)
