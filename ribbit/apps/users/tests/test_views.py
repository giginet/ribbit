from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from django.conf import settings

from ribbit.apps.rooms.factory_boy import RoomFactory, RoleFactory
from ribbit.apps.users.factory_boy import UserFactory

from ribbit.apps.users.models import User

class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='kawaztan', password='password')

    def test_login_exist(self):
        """Test users can access to the login page."""
        c = Client()
        response = c.get(reverse('users_user_login'))
        self.assertEqual(response.status_code, 200, "Users can access login view")

    def test_login_correctly(self):
        """Test User can authenticate via login view."""
        c = Client()
        response = c.post(reverse('users_user_login'), {
            'username' : 'kawaztan',
            'password' : 'password'
        })
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL, status_code=302, target_status_code=301)

    def test_login_failed(self):
        """Test login view when user authentication is failed"""
        c = Client()
        response = c.post(reverse('users_user_login'), {
            'username' : 'kawaztan',
            'password' : 'incorrect_password'
        })
        self.assertContains(response, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

class UserLogoutViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.user.set_password("password")
        self.user.save()

    def test_logout(self):
        """Test user can logout via LogoutView"""
        c = Client()
        self.assertTrue(c.login(username=self.user.username, password='password'))
        self.assertTrue(c.session.has_key('_auth_user_id'))
        response = c.post(reverse('users_user_logout'))
        self.assertFalse(c.session.has_key('_auth_user_id'))
        self.assertRedirects(response, settings.LOGIN_URL, status_code=302, target_status_code=301)

    def test_cannot_logout(self):
        """Test unauthorized user can't logout via LogoutView"""
        c = Client()
        response = c.post(reverse('users_user_logout'))
        self.assertRedirects(response, settings.LOGIN_URL, status_code=302, target_status_code=301)

    def test_get_logout_view(self):
        """Test user can't access LogoutView by get method"""
        c = Client()
        response = c.get(reverse('users_user_logout'))
        self.assertEqual(response.status_code, 405)
