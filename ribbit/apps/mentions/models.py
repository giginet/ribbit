from django.db import models
from django.utils.translation import ugettext as _
from ribbit.apps.users.models import User
from ribbit.apps.messages.models import Message

class MentionManager(models.Manager):
    def create_from_message(self, message):
        return None

class Mention(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'))
    message = models.ForeignKey(Message, verbose_name=_('Message'), related_name='mentions')
    in_reply_to = models.ForeignKey(Message, verbose_name=_('In reply to'), null=True, blank=True, related_name='replies')
    is_read = models.BooleanField(verbose_name=_('Read flag'), default=False, null=False, blank=True)

    objects = MentionManager()

    def __unicode__(self):
        return self.message.__unicode__()

    class Meta:
        verbose_name = _('Mention')
        verbose_name_plural = _('Mentions')