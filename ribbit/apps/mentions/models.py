import re
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from ribbit.apps.users.models import User
from ribbit.apps.messages.models import Message

class MentionManager(models.Manager):
    MENTION_REGEX = r'@(?P<username>[\w-]+)'

    def create_from_message(self, message, in_reply_to=None):
        names = re.findall(self.MENTION_REGEX, message.body)
        if 'all' in names:
            room_members = message.room.members.values_list('username')
            names.remove('all')
            [names.append(member[0]) for member in room_members]
        users_set = set(names) # unique!
        pks = []
        try:
            users = User.objects.filter(username__in=users_set)
            for user in users:
                mention = self.create(message=message, in_reply_to=in_reply_to, user=user)
                pks.append(mention.pk)
        except:
            pass
        return self.filter(pk__in=pks).order_by('user__pk')

class Mention(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'))
    message = models.ForeignKey(Message, verbose_name=_('Message'), related_name='mentions')
    in_reply_to = models.ForeignKey(Message, verbose_name=_('In reply to'), null=True, blank=True, related_name='replies')
    is_read = models.BooleanField(verbose_name=_('Read flag'), default=False, null=False, blank=True)

    objects = MentionManager()

    def __unicode__(self):
        return self.message.__unicode__()

    class Meta:
        ordering = ('-message__created_at',)
        verbose_name = _('Mention')
        verbose_name_plural = _('Mentions')

@receiver(post_save, sender=Message)
def create_mention(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        Mention.objects.create_from_message(instance)
