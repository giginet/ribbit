import os
import json
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.utils.translation import ugettext as _
from django.conf import settings

from easy_thumbnails.fields import ThumbnailerImageField

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

class RoomManager(models.Manager):
    def get_viewable_rooms(self):
        pass

class Room(models.Model):
    """
    Model which indicates Chat room.
    """

    ROOM_SCOPE = (
        ('public', _('Public')),
        ('private', _('Invite Only')),
    )

    def get_room_group_name(self):
        return "room_%s" % self.slug

    def icon_image_path(instance, filename):
        return os.path.join(settings.STATIC_DIR, 'uploads', 'icons', '%s.png' % instance.slug)

    title = models.CharField(max_length=128, verbose_name=_('Title'))
    slug = models.SlugField(max_length=32, verbose_name=_('Slug'), unique=True)
    description = models.CharField(max_length=1024, verbose_name=_('Description'), null=True, blank=True)
    scope = models.CharField(choices=ROOM_SCOPE, verbose_name=_('Scope'), default='public', max_length=16)
    author = models.ForeignKey(User, verbose_name=_('Author'), related_name='created_rooms')
    members = models.ManyToManyField(User, verbose_name=_('Members'), related_name='joined rooms', through=Role, editable=False)
    group = models.ForeignKey(Group, verbose_name=_('Member group'), editable=False, unique=True, null=True, blank=False)
    icon = ThumbnailerImageField(verbose_name=_('Icon image'), null=True, blank=True, upload_to=icon_image_path)
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Date created'))
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date updated'))

    objects = RoomManager()

    def __unicode__(self):
        return "%(title)s(%(scope)s)" % {'title' : self.title, 'scope' : dict(self.ROOM_SCOPE)[self.scope]}

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def serialize(self):
        """
        Return a dictionary which contains each fields
        @return dict
        """
        dict = {
            'pk': self.pk,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'scope': self.scope,
            'icon': ''
        }
        if self.icon:
            dict['icon'] = os.path.join(settings.STATIC_URL, os.path.relpath(self.icon['thumbnail'].url, settings.STATIC_DIR))
        return dict

    @models.permalink
    def get_absolute_url(self):
        return ('rooms_room_detail', (), {'slug' : self.slug})

    def add_member(self, user, permission=Role.MEMBER):
        """
        Add the member to this room
        @param user User who is added to this room.
        @param permission Integer the integer which indicate to member permission.
        @return boolean value which indicates to whether success or not
        """
        if not self.is_member(user):
            role = Role.objects.create(room=self, user=user, permission=permission)
            return True
        return False

    def remove_member(self, user):
        """
        Remove the member from this room
        @param user User who is removed from this room
        @return boolean value which indicates to whether success or not
        """
        if self.is_member(user):
            role = Role.objects.get(room=self, user=user)
            role.delete()
            return True
        return False

    def is_member(self, user):
        """
        Return whether the user is a member or not
        @param user
        @return boolean
        """
        return Role.objects.filter(room=self, user=user).count() > 0

    def add_message(self, body, author):
        """
        Add message to this room
        @param body string message body
        @param author user
        """
        from ribbit.apps.messages.models import Message
        return Message.objects.create(room=self, body=body, author=author)

    def is_joinable(self, user):
        """
        Return whether passed user can join to this room or not
        @param user
        @return boolean
        """
        # ToDo : Implement member invitation and join request
        return self.scope == 'public'

    def is_viewable(self, user):
        """
        Return whether passed user can view this room or not
        @param user
        @return boolean
        """
        try:
            role = Role.objects.get(room=self, user=user)
            return role.permission >= Role.VIEWER
        except:
            return False

    def is_writable(self, user):
        """
        Return whether passed user can write to this room or not
        @param user
        @return boolean
        """
        try:
            role = Role.objects.get(room=self, user=user)
            return role.permission >= Role.MEMBER
        except:
            return False

    def is_administrable(self, user):
        """
        Return whether passed user can manage this room or not
        @param user
        @return boolean
        """
        try:
            role = Role.objects.get(room=self, user=user)
            return role.permission >= Role.ADMIN
        except:
            return False

    @property
    def administrators(self):
        """
        Get users who can manage this room
        @return QuerySets contains room admin users.
        """
        return self.members.filter(role__permission=Role.ADMIN)

@receiver(post_save, sender=Room)
def create_group(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        group, created = Group.objects.get_or_create(name=instance.get_room_group_name())
        instance.group = group

@receiver(post_save, sender=Room)
def add_admin(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        role = Role(user=instance.author, room=instance, permission=Role.ADMIN)
        role.save()
