from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from lostboard.views.posts_view import PostsView
from lostboard.views.posts.comments_view import CommentsView as PostsCommentsView
from lostboard.views.comments_view import CommentsView
from lostboard.views.comments.comments_view import CommentsView as CommentsCommentsView

app_name = 'lostboard'

# base 이름은 view의 단축이름을 만들때 사용한다.
posts_router = DefaultRouter(trailing_slash=False)
posts_router.register(r'posts', PostsView, basename='posts')
posts_comments_router = NestedDefaultRouter(posts_router, r'posts', lookup='post')
posts_comments_router.register(r'comments', PostsCommentsView, basename='posts_comments')

# lookup에 _pk가 붙여져진다
comments_router = DefaultRouter(trailing_slash=False)
comments_router.register(r'comments', CommentsView, basename='comments')
comments_comments_router = NestedDefaultRouter(comments_router, r'comments', lookup='comment')
comments_comments_router.register(r'comments', CommentsCommentsView, basename='comments_comments')

# urlpatterns
urlpatterns = [
    path('', include(posts_router.urls)),
    path('', include(posts_comments_router.urls)),
    path('', include(comments_router.urls)),
    path('', include(comments_comments_router.urls))
]
