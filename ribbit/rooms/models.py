from django.db import models
from django.utils.translation import ugettext as _

u"""
    Model for Chat room.
"""
class Room(models.Model):

    ROOM_SCOPE = (
        ('public', _('Public')),
        ('private', _('Invite Only')),
    )

    def icon_image_path(filename):
        return ''

    title = models.CharField(max_length=128, verbose_name=_('Title'), null=False, blank=False)
    description = models.CharField(max_length=1024, verbose_name=_('Description'), null=True, blank=True)
    scope = models.CharField(choices=ROOM_SCOPE, verbose_name=_('Scope'), default='public', max_length=16)
    icon_image = models.ImageField(verbose_name=_('Icon image'), null=True, blank=True, upload_to=icon_image_path)
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Date created'))
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date updated'))

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'