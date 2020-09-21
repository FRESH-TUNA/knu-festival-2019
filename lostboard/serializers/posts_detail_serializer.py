from rest_framework import serializers
from lostboard.models import Post, Comment
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

class PostsDetailSerializer(serializers.ModelSerializer):
    # comments = serializers.HyperlinkedIdentityField(
    #     view_name='lostboard:posts_comments-list',
    #     lookup_url_kwarg='post_pk',
    #     lookup_field='pk'
    # )

    comments = serializers.SerializerMethodField()

    url = serializers.HyperlinkedIdentityField(view_name='lostboard:posts-detail')

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_comments(self, obj):
        class CommentsSerializer(serializers.Serializer):
            url = serializers.HyperlinkedIdentityField(
                view_name='lostboard:posts_comments-list',
                lookup_url_kwarg='post_pk',
                lookup_field='pk'
            )
            count = serializers.SerializerMethodField()
            
            def get_count(self, obj):
                return obj.comments.count() 
        return CommentsSerializer(obj, context=self.context).data

    def update(self, instance, validated_data):
        # image가 없으면 update 하지 않음
        if validated_data.get('image') == None:
            validated_data.pop('image')
        return super().update(instance, validated_data)
