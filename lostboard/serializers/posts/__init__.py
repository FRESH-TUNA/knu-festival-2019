from rest_framework import serializers
from lostboard.models import Post, Comment

class PostsListSerializer(serializers.ModelSerializer):
    # inline class
    class CommentsSerializerMethodField(serializers.SerializerMethodField):
        def to_representation(self, value):
            method = getattr(self.parent, self.method_name)
            return {'count': method(value)}

    comments = CommentsSerializerMethodField('get_comments_count')

    class Meta:
        model = Post
        fields = '__all__'

    def get_comments_count(self, obj):
        return obj.comments.count()

class PostsDetailSerializer(serializers.ModelSerializer):
    from .comments import PostsCommentsSerializer

    comments = PostsCommentsSerializer(required=False, many=True)

    class Meta:
        model = Post
        fields = '__all__'
