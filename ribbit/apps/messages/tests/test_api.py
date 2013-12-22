import json
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from django.conf import settings

from ribbit.apps.rooms.factory_boy import RoomFactory, RoleFactory
from ribbit.apps.users.factory_boy import UserFactory
from ribbit.apps.messages.factory_boy import MessageFactory

class MessageAPITestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.user.set_password('password')
        self.user.save()

    def test_not_authorized_user(self):
        """Test not authorized user cant access to the API"""
        c = Client()
        response = c.get(reverse('message-list'))
        dict = json.loads(response.content)
        self.assertIsNotNone(dict.get('detail'))
        self.assertEqual(response.status_code, 403)

    def test_messages_list_with_invalid_room_id(self):
        """Test authorized user without Room ID can't get message list."""
        c = Client()
        message = MessageFactory.create(body='hello')
        self.assertTrue(c.login(username=self.user.username, password='password'))
        response = c.get(reverse('message-list'))
        error = json.loads(response.content)
        self.assertDictContainsSubset(error, {'detail':'Room ID is invalid'})
        self.assertEqual(response.status_code, 404)

    def test_messages_list(self):
        """Test authorized user can get message list"""
        c = Client()
        message = MessageFactory.create(body='hello')
        room = message.room
        self.assertTrue(c.login(username=self.user.username, password='password'))
        response = c.get(reverse('message-list'), data={'room':room.slug})
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['body'], 'hello')
        self.assertEqual(response_json[0]['room']['slug'], room.slug)
        self.assertEqual(response_json[0]['room']['id'], room.id)
        self.assertEqual(response_json[0]['author']['id'], message.author.id)
        self.assertEqual(response_json[0]['author']['username'], message.author.username)

    def test_messages_list_with_since(self):
        """Test Users can get list with since id"""
        c = Client()
        room = RoomFactory.create()
        messages = [MessageFactory.create(room=room) for i in xrange(5)]
        self.assertTrue(c.login(username=self.user.username, password='password'))
        response = c.get(reverse('message-list'), data={'room':room.slug})
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 5)
        response = c.get(reverse('message-list'), data={'room':room.slug, 'since':messages[2].pk})
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)
        response = c.get(reverse('message-list'), data={'room':room.slug, 'since':messages[4].pk})
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 0)

    def test_messages_list_with_count(self):
        """Test Users can get list with count"""
        c = Client()
        room = RoomFactory.create()
        messages = [MessageFactory.create(room=room) for i in xrange(5)]
        self.assertTrue(c.login(username=self.user.username, password='password'))
        response = c.get(reverse('message-list'), data={'room':room.slug})
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 5)
        response = c.get(reverse('message-list'), data={'room':room.slug, 'count':2})
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)

    def test_messages_list_with_invalid_since(self):
        """Test Users get 404 list with invalid since id"""
        c = Client()
        room = RoomFactory.create()
        messages = [MessageFactory.create(room=room) for i in xrange(5)]
        self.assertTrue(c.login(username=self.user.username, password='password'))
        response = c.get(reverse('message-list'), data={'room':room.slug, 'since':-100})
        self.assertEqual(response.status_code, 404)

    def test_messages_list_with_invalid_count(self):
        """Test Users get 404 list with invalid count"""
        c = Client()
        room = RoomFactory.create()
        messages = [MessageFactory.create(room=room) for i in xrange(5)]
        self.assertTrue(c.login(username=self.user.username, password='password'))
        response = c.get(reverse('message-list'), data={'room':room.slug, 'count':"aaaaaaa"})
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json), 5)
        self.assertEqual(response_json[0]['room']['slug'], room.slug)
        self.assertEqual(response_json[0]['room']['id'], room.id)
        self.assertEqual(response_json[0]['author']['id'], messages[4].author.id)
        self.assertEqual(response_json[0]['author']['username'], messages[4].author.username)
