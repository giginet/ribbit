import os
import re
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _
from django.conf import settings

from easy_thumbnails.fields import ThumbnailerImageField

class User(AbstractUser):

    USERNAME_REGEX = r'^[\w-]+$'

    def avatar_image_path(instance, filename):
        return os.path.join(settings.STATIC_DIR, 'uploads', 'avatars', '%s.png' % instance.username)

    screen_name = models.CharField(verbose_name=_('Screen Name'), max_length=32, null=False, blank=True)
    avatar = ThumbnailerImageField(verbose_name=_('Avatar'), null=True, blank=True, upload_to=avatar_image_path)
    twitter = models.CharField(verbose_name=_('Twitter ID'), max_length=15, null=True, blank=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __unicode__(self):
        return "%s(%s)" % (self.screen_name, self.username)

    def avatar_url(self):
        return ''
        # if not self.avatar:
        #     return ''
        # return os.path.join(settings.STATIC_URL, os.path.relpath(self.avatar['thumbnail'].url, settings.STATIC_DIR))

    def clean(self):
        if not re.match(self.USERNAME_REGEX, self.username):
            raise ValidationError('Username must contain alphabetical characters only.')
        elif self.username in settings.USERNAME_BLACKLISTS:
            raise ValidationError("""username '%s' is not permitted.""" % self.username)
        super(User, self).clean()

    def save(self, *args, **kwargs):
        if not self.screen_name:
            self.screen_name = self.username
        self.full_clean()
        return super(User, self).save(*args, **kwargs)

    def serialize(self):
        dict = {
            'pk': self.pk,
            'username': self.username,
            'screen_name': self.screen_name,
            'twitter': self.twitter,
            'avatar': ''
        }
        return dict

    @models.permalink
    def get_absolute_url(self):
        return ('users_user_detail', (), {'username' : self.username})
