from serializers import UserSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from models import User

class UserViewSet(ViewSet):
    """
    The ViewSet of User model
    """
    def list(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)