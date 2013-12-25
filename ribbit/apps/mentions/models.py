from django.db import models
from django.utils.translation import ugettext as _
from ribbit.apps.users.models import User
from ribbit.apps.messages.models import Message

class MentionManager(models.Manager):
    def create_from_message(self, message):
        return None

class Mention(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'))
    message = models.ForeignKey(Message, verbose_name=_('Message'))
    in_reply_to = models.ForeignKey(Message, verbose_name=_('In reply to'), null=True, blank=True)
    is_read = models.BooleanField(verbose_name=_('Read flag'), default=False, null=False, blank=True)

    objects = MentionManager()

    def __unicode__(self):
        return self.message.__unicode__()
