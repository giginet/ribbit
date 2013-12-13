from django.test import TestCase
from django.contrib.auth.models import Group

from models import Room, Role
from users.factory_boy import UserFactory
from factory_boy import RoomFactory

class RoomCreationTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.user.save()

    def test_can_create_room(self):
        """Test whether can create new room and get fields."""
        room = RoomFactory.create()
        self.assertEqual(room.title, 'Test Chat', "Can get room's title")
        self.assertEqual(room.slug, 'test-chat', "Can get room's slug")
        self.assertEqual(room.scope, 'public', "Can get room's scope and default value will be public.")
        self.assertEqual(room.author.username, 'kawaztan', "Can get room's author")

    def test_group_was_created_when_room_was_created(self):
        """Test new group was created on room creation."""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        group = Group.objects.get(name='room_%s' % room.slug)
        self.assertIsNotNone(group, "The group was created")

    def test_author_will_be_an_admin_of_room(self):
        """Test member will be an admin of created room."""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        role = Role.objects.get(user=self.user, room=room, permission='admin')

