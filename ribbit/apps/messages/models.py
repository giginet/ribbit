from django.db import models
from django.utils.translation import ugettext as _

from ribbit.apps.rooms.models import Room
from ribbit.apps.users.models import User

class Message(models.Model):

    body = models.CharField(verbose_name=_('Body'), max_length=4096)
    room = models.ForeignKey(Room, verbose_name=_('Room'))
    author = models.ForeignKey(User, verbose_name=_('Author'))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Date created'))
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date updated'))

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __unicode__(self):
        return "%s (%s)" % (self.body[:100], self.author.username)
