from rest_framework import serializers
from lostboard.models import Post, Comment

class PostsDetailSerializer(serializers.ModelSerializer):
    from .posts.comments_list_serializer import CommentsListSerializer

    comments = CommentsListSerializer(required=False, many=True)
    url = serializers.HyperlinkedIdentityField(view_name='lostboard:posts-detail')

    class Meta:
        model = Post
        fields = '__all__'
