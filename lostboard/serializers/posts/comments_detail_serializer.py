from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from lostboard.models import Comment

class CommentsDetailSerializer(serializers.ModelSerializer):
    # post_pk: url에서 받는 인자, 'post__pk': parent model의 기본키 접근을 위한 ORM 문법
    url = NestedHyperlinkedIdentityField(
        view_name='lostboard:posts_comments-detail',
        parent_lookup_kwargs={'post_pk': 'post__pk'}
    )

    class Meta:
        model = Comment
        fields = '__all__'
