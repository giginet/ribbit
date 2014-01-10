import json
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from ribbit.apps.rooms.tests.factory_boy import RoomFactory
from ribbit.apps.users.tests.factory_boy import UserFactory
from ribbit.apps.messages.tests.factory_boy import MessageFactory
from factory_boy import MentionFactory

class MentionAPITestCase(TestCase):
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
