from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "created", "modified", "title", "body", "user", "likes_count"]

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()
