from rest_framework.generics import RetrieveAPIView

from .models import User
from .serializers import UserSerializer


class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
