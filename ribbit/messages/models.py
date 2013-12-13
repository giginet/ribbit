from django.db import models
from django.utils.translation import ugettext as _

from rooms.models import Room
from users.models import User

class Message(models.Model):

    body = models.CharField(verbose_name=_('Body'), max_length=4096)
    room = models.ForeignKey(Room, verbose_name=_('Room'))
    author = models.ForeignKey(User, verbose_name=_('Author'))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __unicode__(self):
        return "%s (%s)" % (self.body[:100], self.author.username)
