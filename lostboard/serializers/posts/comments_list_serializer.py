from rest_framework import serializers
from lostboard.models import Comment

class CommentsListSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='lostboard:posts_comments-detail')

    class Meta:
        model = Comment
        fields = '__all__'

