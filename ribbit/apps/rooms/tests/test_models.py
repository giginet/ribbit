from django.test import TestCase
from django.contrib.auth.models import Group
from django.db import IntegrityError

from ribbit.apps.users.factory_boy import UserFactory
from ribbit.apps.rooms.models import Room, Role
from ribbit.apps.rooms.factory_boy import RoomFactory

class RoomTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()

    def test_can_create_room(self):
        """Test whether can create new room and get fields."""
        room = RoomFactory.create(slug='test-chat', author=self.user)
        self.assertEqual(room.title, 'Test Chat', "Can get room's title")
        self.assertEqual(room.slug, 'test-chat', "Can get room's slug")
        self.assertEqual(room.scope, 'public', "Can get room's scope and default value will be public.")
        self.assertEqual(room.author, self.user, "Can get room's author")

    def test_group_was_created_when_room_was_created(self):
        """Test new group was created on room creation."""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        group = Group.objects.get(name='room_%s' % room.slug)
        self.assertIsNotNone(group, "The group was created")

    def test_meta_class(self):
        """Test meta class attributes is correct"""
        self.assertEqual(Room._meta.verbose_name.title(), 'Room', 'Meta.verbose_name is correct')
        self.assertEqual(Room._meta.verbose_name_plural.title(), 'Rooms', 'Meta.verbose_name_plural is correct')


    def test_author_will_be_an_admin_of_room(self):
        """Test member will be an admin of created room."""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        role = Role.objects.get(user=self.user, room=room, permission=Role.ADMIN)
        self.assertIsNotNone(role, 'The author will be room admin')

    def test_can_not_create_duplicated_slug(self):
        """Test the room has duplicated slug will not be created."""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        def create_dupliacted_room():
            room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        self.assertRaises(IntegrityError, create_dupliacted_room)

    def test_has_member(self):
        """Test is_member returns correct value"""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        user1 = UserFactory.create(username='mario')
        self.assertFalse(room.is_member(user1), 'is_member returns false')
        room.add_member(user1)
        self.assertTrue(room.is_member(user1), 'is_member returns true')

    def test_can_add_member(self):
        """Test user can be added"""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        user1 = UserFactory.create(username='mario')
        self.assertTrue(room.add_member(user1), 'add_member returns true')
        user2 = UserFactory.create(username='luigi')
        self.assertTrue(room.add_member(user2, permission=Role.VIEWER), 'add_member returns true')
        self.assertEqual(room.members.count(), 3, 'the count of members is correct')
        role = Role.objects.get(room=room, user=user1)
        self.assertEqual(role.permission, Role.MEMBER, 'the default permission is correct')
        role1 = Role.objects.get(room=room, user=user2)
        self.assertEqual(role1.permission, Role.VIEWER, 'the member of permission is correct')

    def test_can_remove_member(self):
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        user1 = UserFactory.create(username='mario')
        room.add_member(user1)
        self.assertTrue(room.remove_member(user1), 'remove_member returns false')
        self.assertEqual(room.members.count(), 1, 'the count of members is correct')

    def test_can_get_suitable_administrators(self):
        """Test administrators property can get suitable users"""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        user1 = UserFactory.create(username='mario')
        user2 = UserFactory.create(username='luigi')
        user3 = UserFactory.create(username='peach')
        room.add_member(user1, permission=Role.ADMIN)
        room.add_member(user2, permission=Role.VIEWER)
        room.add_member(user3, permission=Role.MEMBER)
        self.assertEqual(room.administrators.count(), 2, 'the count of administrators is correct')
        self.assertEqual(room.administrators[0].username, self.user.username)
        self.assertEqual(room.administrators[1].username, 'mario')

    def test_can_not_add_multiple_members(self):
        """Test multiple members can not be added to the room."""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        user1 = UserFactory.create(username='mario')
        self.assertTrue(room.add_member(user1), 'add_member returns true')
        self.assertFalse(room.add_member(user1), 'add_member returns true')

    def test_can_not_remove_non_member(self):
        """Test the member who not join to the room can not be removed"""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        user1 = UserFactory.create(username='mario')
        self.assertFalse(room.remove_member(user1), 'remove_member returns false')

    def test_raise_error_when_create_multiple_role(self):
        """Test the error is raised when multiple roles are created"""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        user1 = UserFactory.create(username='mario')
        role = Role.objects.create(room=room, user=user1)
        def create_role_multiple():
            Role.objects.create(room=room, user=user1, permission=Role.ADMIN)
        self.assertRaises(IntegrityError, create_role_multiple)

    def test_unicode_returns_suitable_name(self):
        """Test __unicode__ returns suitable room name"""
        room = RoomFactory.create()
        self.assertEqual(unicode(room), 'Test Chat(Public)', '__unicode__ retusns name correctly when room scope is public')
        room.scope = 'private'
        self.assertEqual(unicode(room), 'Test Chat(Invite Only)', '__unicode__ retusns name correctly when room scope is private')

    def test_can_get_correct_permission(self):
        """Test correct permission can be returend."""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        user0 = UserFactory.create(username='sonic')
        user1 = UserFactory.create(username='tales')
        user2 = UserFactory.create(username='shadow')
        user3 = UserFactory.create(username='emmy')
        room.add_member(user0, permission=Role.ADMIN)
        room.add_member(user1, permission=Role.MEMBER)
        room.add_member(user2, permission=Role.VIEWER)

        self.assertTrue(room.is_viewable(user0), 'Admin user can view the room')
        self.assertTrue(room.is_viewable(user1), 'Member user can view the room')
        self.assertTrue(room.is_viewable(user2), 'Viewer user can view the room')
        self.assertFalse(room.is_viewable(user3), 'Not member can not view the room')

        self.assertTrue(room.is_writable(user0), 'Admin user can write to the room')
        self.assertTrue(room.is_writable(user1), 'Member user can write to the room')
        self.assertFalse(room.is_writable(user2), 'Viewer user can not write to the room')
        self.assertFalse(room.is_writable(user3), 'Not member can not write to the room')

        self.assertTrue(room.is_administrable(user0), 'Admin user can manage the room')
        self.assertFalse(room.is_administrable(user1), 'Member user can not manage the room')
        self.assertFalse(room.is_administrable(user2), 'Viewer user can not manage the room')
        self.assertFalse(room.is_administrable(user3), 'Not member can not manage the room')

    def test_is_joinable_returns_correct_value(self):
        """Test is_joinable returns correct value"""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user)
        user0 = UserFactory.build(username='sonic')
        self.assertTrue(room.is_joinable(user0), 'Everyone can join to a public room')

        room1 = RoomFactory.build(scope='private')
        self.assertFalse(room1.is_joinable(user0), 'Anyone can not join to a public room')

    def test_serialize(self):
        """Test serialize() can return correct dict"""
        room = Room.objects.create(title='Test Chat', slug='test-chat', author=self.user, description="This is a test chat")
        self.assertDictEqual(room.serialize(), {
            'pk': room.pk,
            'icon': '',
            'title': 'Test Chat',
            'slug': 'test-chat',
            'scope': 'public',
            'description': 'This is a test chat'
        }, 'serialize() returns correct dict')
