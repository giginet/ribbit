from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from django.conf import settings

from ribbit.apps.rooms.factory_boy import RoomFactory, RoleFactory
from ribbit.apps.rooms.models import Room, Role
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
        response = c.post(url)
        self.assertRedirects(response, "%s?next=%s" % (settings.LOGIN_URL, url), status_code=302, target_status_code=301)

    def test_post_form(self):
        """Test room was created when user post to the form"""
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        url = reverse('rooms_room_create')
        response = c.post(url, {
            'title' : 'My Chat',
            'slug' : 'my-chat',
            'description' : 'This is my chat',
            'scope' : 'public'
        })
        room = Room.objects.get(slug='my-chat')
        self.assertRedirects(response, room.get_absolute_url(), status_code=302, target_status_code=200)
        self.assertEqual(room.title, 'My Chat')
        self.assertEqual(room.slug, 'my-chat')
        self.assertEqual(room.description, 'This is my chat')
        self.assertEqual(room.author, self.user)
        self.assertEqual(room.scope, 'public')

    def test_post_form_with_blank(self):
        """Test room was created when user post to the form"""
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        url = reverse('rooms_room_create')
        response = c.post(url, {
        })
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'slug', 'This field is required.')
        self.assertFormError(response, 'form', 'scope', 'This field is required.')
        get_room = lambda :Room.objects.get(slug='my-chat')
        self.assertRaises(Exception, get_room)

    def test_post_form_with_invalid_author(self):
        """Test room was created when user post to the form"""
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        url = reverse('rooms_room_create')
        response = c.post(url, {
            'title' : 'My Chat',
            'slug' : 'my-chat',
            'description' : 'This is my chat',
            'scope' : 'public',
            'author' : self.another_user
        })
        room = Room.objects.get(slug='my-chat')
        self.assertRedirects(response, room.get_absolute_url(), status_code=302, target_status_code=200)
        self.assertEqual(room.title, 'My Chat')
        self.assertEqual(room.slug, 'my-chat')
        self.assertEqual(room.description, 'This is my chat')
        self.assertEqual(room.author, self.user)
        self.assertEqual(room.scope, 'public')

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
        self.assertContains(response, 'Permission Denied', status_code=403)

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

class RoomUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create(username='kawaztan')
        self.user.set_password('password')
        self.user.save()

    def test_not_authorized(self):
        """Not authorized user can't access to the RoomUpdateView"""
        room = RoomFactory.create()
        c = Client()
        url = reverse('rooms_room_update', args=(room.slug,))
        response = c.get(url)
        self.assertRedirects(response, "%s?next=%s" % (settings.LOGIN_URL, url), status_code=302, target_status_code=301)

    def test_not_admin(self):
        """Not admin user can't access to the RoomUpdateView"""
        room = RoomFactory.create()
        room.add_member(self.user)
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        self.assertTrue(room.is_writable(self.user))
        self.assertFalse(room.is_administrable(self.user))
        url = reverse('rooms_room_update', args=(room.slug,))
        response = c.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, 'Permission Denied', status_code=403)

    def test_can_access(self):
        """Admin user can access to the RoomUpdateView"""
        room = RoomFactory.create()
        room.add_member(self.user, Role.ADMIN)
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        self.assertTrue(room.is_administrable(self.user))
        url = reverse('rooms_room_update', args=(room.slug,))
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rooms/room_form.html')

    def test_can_update(self):
        """Test user can update the room via RoomUpdateView"""
        room = RoomFactory.create()
        room.add_member(self.user, Role.ADMIN)
        c = Client()
        self.assertTrue(c.login(username='kawaztan', password='password'))
        self.assertTrue(room.is_administrable(self.user))
        url = reverse('rooms_room_update', args=(room.slug,))
        response = c.post(url, {
            'title' : 'new Title',
            'description' : 'new Description',
            'is_active' : False
        })
        room = Room.objects.get(slug=room.slug)
        self.assertRedirects(response, room.get_absolute_url(), status_code=302, target_status_code=200)
        self.assertFalse(room.is_active)
        self.assertEqual(room.title, 'new Title')
        self.assertEqual(room.description, 'new Description')
