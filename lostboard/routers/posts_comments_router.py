from rest_framework_nested.routers import NestedSimpleRouter
from lostboard.views.posts.comments_view import CommentsView
from lostboard.routers.posts_router import posts_router

# lookup에 _pk가 붙여져진다
posts_comments_router = NestedSimpleRouter(posts_router, r'posts', lookup='post')
posts_comments_router.register(r'comments', CommentsView, basename='posts_comments')
