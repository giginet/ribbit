import os
import json
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _
from django.core import serializers
from django.conf import settings

from easy_thumbnails.fields import ThumbnailerImageField

class User(AbstractUser):

    def avatar_image_path(instance, filename):
        return os.path.join(settings.STATIC_DIR, 'uploads', 'avatars', '%s.png' % instance.username)

    screen_name = models.CharField(verbose_name=_('Screen Name'), max_length=32)
    avatar = ThumbnailerImageField(verbose_name=_('Avatar'), null=True, blank=True, upload_to=avatar_image_path)
    twitter = models.CharField(verbose_name=_('Twitter ID'), max_length=15, null=True, blank=True)

    def serialize(self):
        return {
            'pk': self.pk,
            'username': self.username,
            'screen_name': self.screen_name,
            'twitter': self.twitter,
            'avatar': os.path.join(settings.STATIC_URL, os.path.relpath(self.avatar['thumbnail'].url, settings.STATIC_DIR))
        }
