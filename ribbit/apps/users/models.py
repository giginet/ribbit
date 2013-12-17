import json
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _
from django.core import serializers

class User(AbstractUser):

    def user_avatar_path(filename):
        return ''

    screen_name = models.CharField(verbose_name=_('Screen Name'), max_length=32)
    avatar = models.ImageField(verbose_name=_('Avatar'), null=True, blank=True, upload_to=user_avatar_path)
    twitter = models.CharField(verbose_name=_('Twitter ID'), max_length=15)

    def serialize(self):
        return json.loads(serializers.serialize('json', [self, ], fields=(
            'username',
            'screen_name',
            'twitter',
            'avatar'
        )))[0]