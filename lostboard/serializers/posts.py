from rest_framework import serializers
from lostboard.models import Post

class LostboardPostsIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
