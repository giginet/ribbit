from django.db import models
from django.utils.translation import ugettext as _

u"""
    Model for Char room.
"""
class Room(models.Model):

    ROOM_SCOPE = (
        ('public', _('Public')),
        ('private', _('Invite Only')),
    )

    def icon_image_path(filename):
        return ''

    name = models.CharField(max_length=128, verbose_name=_('Room'), null=False, blank=False)
    scope = models.CharField(choices=ROOM_SCOPE, verbose_name=_('Scope'), default='public', max_length=16)
    icon_image = models.ImageField(verbose_name=_('Icon Image'), null=True, blank=True, upload_to=icon_image_path)
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'