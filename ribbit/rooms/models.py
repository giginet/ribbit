from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

from users.models import User

"""
Model which indicates relations between users and rooms.
"""
class Role(models.Model):

    PERMISSIONS = (
        ('admin', _('View, Write & Administrative')),
        ('writer', _('View & Write')),
        ('viewer', _('View Only'))
    )

    user = models.ForeignKey(User)
    room = models.ForeignKey('Room')
    permission = models.CharField(verbose_name=_('Permission'), choices=PERMISSIONS, max_length=8)

"""
Model which indicates Chat room.
"""
class Room(models.Model):

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

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def save(self, **kwargs):
        group, created = Group.objects.get_or_create(name=self._get_room_group_name())
        self.group = group
        super(Room, self).save(**kwargs)
        role = Role(user=self.author, room=self, permission='admin')
        role.save()

    """
    Get users who can manage this room
    @return QuerySets contains room admin users.
    """
    def administrators(self):
        return self.members.filter(role__permission='admin')