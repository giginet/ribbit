from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from django.conf import settings

from ribbit.apps.rooms.factory_boy import RoomFactory, RoleFactory
from ribbit.apps.users.factory_boy import UserFactory

class RibbitIndexViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create(username='kawaztan')
        self.user.set_password('password')
        self.user.save()

    def test_not_authenticated_user(self):
        """Test not authenticated user redirect to the login view."""
        c = Client()
        url = reverse('ribbit_index')
        response = c.get(url)
        self.assertRedirects(response, reverse('users_user_login'), status_code=301, target_status_code=200)

    def test_authenticated_user(self):
        """Test authenticated user redirect to the lobby view."""
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        response = c.get(reverse('ribbit_index'))
        self.assertRedirects(response, reverse('ribbit_lobby'), status_code=301, target_status_code=200)

class RibbitLobbyViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create(username='kawaztan')
        self.user.set_password('password')
        self.user.save()
        self.room0 = RoomFactory.create(slug='room0', author=self.user)
        self.room1 = RoomFactory.create(slug='room1')
        self.room2 = RoomFactory.create(slug='room2', author=self.user)
        self.room0.save()
        self.room1.save()
        self.room2.save()

    def test_not_authenticated_user(self):
        """Test not authenticated user can't access to the lobby"""
        c = Client()
        url = reverse('ribbit_lobby')
        response = c.get(url)
        self.assertRedirects(response, "%s?next=%s" % (settings.LOGIN_URL, url), status_code=302, target_status_code=301)

    def test_authenticated_user(self):
        """Test the authenticated user can access to the lobby"""
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        url = reverse('ribbit_lobby')
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_context(self):
        """Test lobby view have contexts correctly"""
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        url = reverse('ribbit_lobby')
        response = c.get(url)
        self.assertIsNotNone(response.context.get('joined_rooms'))
        self.assertIsNotNone(response.context.get('not_joined_rooms'))

    def test_joined_rooms(self):
        """Test joined_rooms has correct rooms."""
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        url = reverse('ribbit_lobby')
        response = c.get(url)
        qs = response.context.get('joined_rooms')
        self.assertEqual(len(qs), 2)
        self.assertEqual(qs[0], self.room0)
        self.assertEqual(qs[1], self.room2)

    def test_not_joined_rooms(self):
        """Test not joined_rooms has correct rooms."""
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        url = reverse('ribbit_lobby')
        response = c.get(url)
        qs = response.context.get('not_joined_rooms')
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0], self.room1)
