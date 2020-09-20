from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from lostboard.models import Comment

class CommentsDetailSerializer(serializers.ModelSerializer):
    # post_pk: url에서 받는 인자, 'post__pk': parent model의 기본키 접근을 위한 ORM 문법
    # comments = NestedHyperlinkedIdentityField(
    #     view_name='lostboard:comments_comments-detail',
    #     parent_lookup_kwargs={'post_pk': 'post__pk'}
    # )

    # lookup_url_kwarg 는 router에서의 변수
    # lookup_field는 serializer의 model의 기본키
    # lookup_field orm 사용가능! ex: post__pk
    comments = serializers.HyperlinkedIdentityField(
        view_name='lostboard:comments_comments-list',
        lookup_url_kwarg='comment_pk',
        lookup_field='pk'
    )

    url = serializers.HyperlinkedIdentityField(view_name='lostboard:comments-detail')

    class Meta:
        model = Comment
        fields = '__all__'
