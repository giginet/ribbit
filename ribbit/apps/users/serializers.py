from rest_framework import serializers
from models import User

class UserSerializer(serializers.ModelSerializer):

    avatar_urls = serializers.CharField(source='avatar_url', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'twitter', 'screen_name', 'avatar_urls')