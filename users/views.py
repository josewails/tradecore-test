from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, GenericAPIView

from .models import User
from .serializers import UserSerializer, UserSignupSerializer


class UserSignupView(GenericAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            refresh = serializer.create(serializer.validated_data)
            return Response(refresh)

        else:
            return Response(dict(errors=serializer.errors), status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
