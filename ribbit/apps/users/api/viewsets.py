from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from ribbit.apps.users.api.serializers import UserSerializer
from ribbit.apps.users.models import User


class UserViewSet(ViewSet):
    """
    The ViewSet of User model
    """
    def list(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)