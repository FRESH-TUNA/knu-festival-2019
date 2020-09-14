from rest_framework.routers import DefaultRouter
from lostboard.views.posts_view import PostsView

# base 이름은 view의 단축이름을 만들때 사용한다.
posts_router = DefaultRouter(trailing_slash=False)
posts_router.register(r'posts', PostsView, basename='posts')
