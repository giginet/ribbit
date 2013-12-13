from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

from ribbit.apps.users.models import User

class Role(models.Model):
    """
    Model which indicates relations between users and rooms.
    """

    ADMIN = 2
    MEMBER = 1
    VIEWER = 0

    PERMISSIONS = (
        (ADMIN, _('View, Write & Administrative')),
        (MEMBER, _('View & Write')),
        (VIEWER, _('View Only'))
    )

    user = models.ForeignKey(User)
    room = models.ForeignKey('Room')
    permission = models.SmallIntegerField(verbose_name=_('Permission'), choices=PERMISSIONS, default=MEMBER)

    def __unicode__(self):
        return "%s - %s" % (self.room.title, self.user.username)

    class Meta:
        unique_together = (('room', 'user'),)


class Room(models.Model):
    """
    Model which indicates Chat room.
    """

    ROOM_SCOPE = (
        ('public', _('Public')),
        ('private', _('Invite Only')),
    )

    def _get_room_group_name(self):
        return "room_%s" % self.slug

    def icon_image_path(filename):
        return ''

    title = models.CharField(max_length=128, verbose_name=_('Title'))
    slug = models.SlugField(max_length=32, verbose_name=_('Slug'), unique=True)
    description = models.CharField(max_length=1024, verbose_name=_('Description'), null=True, blank=True)
    scope = models.CharField(choices=ROOM_SCOPE, verbose_name=_('Scope'), default='public', max_length=16)
    author = models.ForeignKey(User, verbose_name=_('Author'), related_name='created_rooms')
    members = models.ManyToManyField(User, verbose_name=_('Members'), related_name='joined rooms', through=Role, editable=False)
    group = models.ForeignKey(Group, verbose_name=_('Member group'), editable=False, unique=True)
    icon_image = models.ImageField(verbose_name=_('Icon image'), null=True, blank=True, upload_to=icon_image_path)
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Date created'))
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date updated'))

    def __unicode__(self):
        return "%(title)s(%(scope)s)" % {'title' : self.title, 'scope' : dict(self.ROOM_SCOPE)[self.scope]}

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    @models.permalink
    def get_absolute_url(self):
        return ('rooms_room_detail', (), {'slug' : self.slug})

    def save(self, **kwargs):
        group, created = Group.objects.get_or_create(name=self._get_room_group_name())
        self.group = group
        super(Room, self).save(**kwargs)
        role = Role(user=self.author, room=self, permission=Role.ADMIN)
        role.save()

    def add_member(self, user, permission=Role.MEMBER):
        """
        Add the member to this room
        @param user User who is added to this room.
        @param permission Integer the integer which indicate to member permission.
        @return boolean value which indicates to whether success or not
        """
        if not self.has_member(user):
            role = Role.objects.create(room=self, user=user, permission=permission)
            return True
        return False

    def remove_member(self, user):
        """
        Remove the member from this room
        @param user User who is removed from this room
        @return boolean value which indicates to whether success or not
        """
        if self.has_member(user):
            role = Role.objects.get(room=self, user=user)
            role.delete()
            return True
        return False

    def has_member(self, user):
        """
        Return whether the user is a member or not
        @param user
        @return boolean
        """
        return Role.objects.filter(room=self, user=user).count() > 0

    @property
    def administrators(self):
        """
        Get users who can manage this room
        @return QuerySets contains room admin users.
        """
        return self.members.filter(role__permission=Role.ADMIN)