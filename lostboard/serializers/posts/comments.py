from rest_framework import serializers
from lostboard.models import Comment

class PostsCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
