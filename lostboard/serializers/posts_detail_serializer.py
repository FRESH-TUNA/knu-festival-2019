from rest_framework import serializers
from lostboard.models import Post, Comment

class PostsDetailSerializer(serializers.ModelSerializer):
    from .comments import PostsCommentsSerializer

    comments = PostsCommentsSerializer(required=False, many=True)

    class Meta:
        model = Post
        fields = '__all__'
