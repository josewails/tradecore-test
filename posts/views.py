from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Post, Like
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=False, methods=["post"], url_path=r'(?P<pk>\d+)/likes_update/(?P<action>(like|unlike))')
    def likes_update(self, request, *args, **kwargs):
        pk, like_action = kwargs.get("pk"), kwargs.get("action")
        post = Post.objects.filter(pk=pk).first()
        user = request.user

        if post:
            if like_action == "like":
                Like.objects.get_or_create(user=user, post=post)
            elif like_action == "unlike":
                Like.objects.filter(user=user, post=post).delete()
            else:
                return Response(dict(detail="Invalid like action"), status=status.HTTP_400_BAD_REQUEST)

            return Response(PostSerializer(post).data)
        else:
            return Response(dict(detail=f"Post with id {pk} not found"), status=status.HTTP_404_NOT_FOUND)
