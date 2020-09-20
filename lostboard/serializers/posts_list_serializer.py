from rest_framework import serializers
from lostboard.models import Post, Comment

class PostsListSerializer(serializers.ModelSerializer):
    # inline class
    class CommentsSerializerMethodField(serializers.SerializerMethodField):
        def to_representation(self, value):
            method = getattr(self.parent, self.method_name)
            return {'count': method(value)}

    comments = CommentsSerializerMethodField('get_comments_count')
    url = serializers.HyperlinkedIdentityField(view_name='lostboard:posts-detail')

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_comments_count(self, obj):
        return obj.comments.count()
