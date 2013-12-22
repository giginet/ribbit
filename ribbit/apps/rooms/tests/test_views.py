from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from django.conf import settings

from ribbit.apps.rooms.factory_boy import RoomFactory, RoleFactory
from ribbit.apps.users.factory_boy import UserFactory

class RoomCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create(username='kawaztan')
        self.user.set_password('password')
        self.user.save()
        self.another_user = UserFactory.create()

    def test_authorized_user_can_view_room_creation(self):
        """Test authorized user can show RoomCreateView"""
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        response = c.get(reverse('rooms_room_create'))
        self.assertEqual(response.status_code, 200, "Authorized user can show RoomCreateView")

    def test_not_authorized_user_cant_view_room_creation(self):
        """Test not authorized user can't show RoomCreationView"""
        c = Client()
        url = reverse('rooms_room_create')
        response = c.get(url)
        self.assertRedirects(response, "%s?next=%s" % (settings.LOGIN_URL, url), status_code=302, target_status_code=301)

class RoomDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create(username='kawaztan')
        self.user.set_password('password')
        self.user.save()
        self.another_user = UserFactory.create()

    def test_not_authorized_user_cant_view_any_room(self):
        """Test not authorized user can't access to any rooms."""
        c = Client()
        room = RoomFactory.create()
        url = reverse('rooms_room_detail', args=(room.pk,))
        response = c.get(url)
        self.assertRedirects(response, "%s?next=%s" % (settings.LOGIN_URL, url), status_code=302, target_status_code=301)

    def test_authorized_user_can_access_public_room(self):
        """Test a authorized user can access to public rooms."""
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        room = RoomFactory.create(author=self.another_user)
        url = reverse('rooms_room_detail', args=(room.slug,))
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_not_permitted_user_cant_access_private_room(self):
        """Test not permitted user can't access to the private room"""
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        room = RoomFactory.create(scope='private', author=self.another_user)
        url = reverse('rooms_room_detail', args=(room.slug,))
        response = c.get(url)
        self.assertEqual(response.status_code, 403)

    def test_permitted_user_can_access_private_room(self):
        """Test the permitted user can access to the private rooms."""
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        room = RoomFactory.create(scope='private', author=self.another_user)
        role = RoleFactory.create(room=room, user=self.user)
        url = reverse('rooms_room_detail', args=(room.slug,))
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rooms/room_detail.html')

    def test_admin_user_can_access_owned_room(self):
        """Test the admin users can access to the their managed rooms."""
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        room = RoomFactory.create(scope='private', author=self.user)
        url = reverse('rooms_room_detail', args=(room.slug,))
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rooms/room_detail.html')

    def test_not_member(self):
        """Test user become a room member when user access to joinable rooms."""
        room = RoomFactory.create()
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        self.assertFalse(room.is_member(self.user))
        url = reverse('rooms_room_detail', args=(room.slug,))
        response = c.get(url)
        self.assertTrue(room.is_member(self.user))
