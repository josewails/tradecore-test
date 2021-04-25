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


class UserDetailView(GenericAPIView):

    def get(self, request, pk=None):
        if pk:
            user = User.objects.filter(pk=pk).first()

        else:
            user = request.user

        if not user:
            return Response(dict(errors=dict(error=["User not found"])), status=status.HTTP_404_NOT_FOUND)

        return Response(UserSerializer(user).data)
