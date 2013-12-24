# -*- coding: utf-8 -*-
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

class UserDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.user.set_password('password')
        self.user.save()

    def test_unauthorized_user(self):
        """Test unauthorized user can't access user detail"""
        c = Client()
        url = reverse('users_user_detail', args=(self.user.username,))
        response = c.get(url)
        self.assertRedirects(response, "%s?next=%s" % (settings.LOGIN_URL, url), status_code=302, target_status_code=301)

    def test_not_exist_user(self):
        """Test return 404 when user access to the not exist user page."""
        c = Client()
        self.assertTrue(c.login(username=self.user.username, password='password'))
        url = reverse('users_user_detail', args=('not_exist_user',))
        response = c.get(url)
        self.assertEqual(response.status_code, 404)

    def test_access(self):
        """Test users can view to access exist user page."""
        c = Client()
        self.assertTrue(c.login(username=self.user.username, password='password'))
        url = reverse('users_user_detail', args=(self.user.username,))
        response = c.get(url)
        self.assertEqual(response.context['object'], self.user)

class UserListViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.user.set_password('password')
        self.user.save()

    def test_unauthorized_user(self):
        """Test unauthorized user can't access UserListView"""
        c = Client()
        url = reverse('users_user_list')
        response = c.get(url)
        self.assertRedirects(response, "%s?next=%s" % (settings.LOGIN_URL, url), status_code=302, target_status_code=301)

    def test_access(self):
        """Test authorized user can access to UserListView"""
        c = Client()
        self.assertTrue(c.login(username=self.user.username, password='password'))
        url = reverse('users_user_list')
        response = c.get(url)
        self.assertEqual(response.context['object_list'][0], self.user)

class UserUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.user.set_password('password')
        self.user.save()

    def test_access(self):
        """Test Users can access to UserUpdateView"""
        c = Client()
        self.assertTrue(c.login(username=self.user.username, password='password'))
        url = reverse('users_user_update')
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user(self):
        """Test unauthorized user can't access UserUpdateView"""
        c = Client()
        url = reverse('users_user_update')
        response = c.get(url)
        self.assertRedirects(response, "%s?next=%s" % (settings.LOGIN_URL, url), status_code=302, target_status_code=301)

    def test_can_update(self):
        """Test authorized users can update their profile."""
        c = Client()
        self.assertTrue(c.login(username=self.user.username, password='password'))
        url = reverse('users_user_update')
        response = c.post(url, {
            'screen_name' : u'かわずたん',
            'first_name' : u'かわず',
            'last_name' : u'井ノ中',
            'twitter' : '@new_kawaztan',
            'email' : 'kawaztan@kawaz.org'
        })
        self.assertRedirects(response, self.user.get_absolute_url(), status_code=302, target_status_code=200)
        user = User.objects.get(username=self.user.username)
        self.assertEqual(user.screen_name, u'かわずたん')
        self.assertEqual(user.first_name, u'かわず')
        self.assertEqual(user.last_name, u'井ノ中')
        self.assertEqual(user.twitter, u'@new_kawaztan')
        self.assertEqual(user.email, u'kawaztan@kawaz.org')

class UserCreateTestCase(TestCase):
    def test_access(self):
        """Test Users can access to UserCreateView"""
        c = Client()
        url = reverse('users_user_create')
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        """User can create new user via UserCreateView."""
        c = Client()
        url = reverse('users_user_create')
        response = c.post(url, {'username' : 'new_user', 'password1' : 'password', 'password2' : 'password'})
        user = User.objects.get(username='new_user')
        self.assertIsNotNone(user)
        self.assertRedirects(response, user.get_absolute_url(), status_code=302, target_status_code=302)

    def test_mismatch_password(self):
        """Test User can't create user with mismatch password"""
        c = Client()
        url = reverse('users_user_create')
        response = c.post(url, {'username' : 'new_user2', 'password1' : 'password', 'password2' : 'missmatch_password'})
        def get_not_exist():
            user = User.objects.get(username='new_user2')
        self.assertRaises(User.DoesNotExist, get_not_exist)
        self.assertEqual(response.status_code, 200)
