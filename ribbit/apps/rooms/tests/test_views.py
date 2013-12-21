from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from django.conf import settings

from ribbit.apps.rooms.factory_boy import RoomFactory
from ribbit.apps.users.factory_boy import UserFactory

from ribbit.apps.users.models import User

class RoomViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='kawaztan', password='password')

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

