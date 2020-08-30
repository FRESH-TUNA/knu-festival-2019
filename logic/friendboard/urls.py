from django.urls import path
from .views.posts import (
    FriendBoardPostListView, 
    FriendBoardPostCreateView, 
    FriendBoardPostDeleteView,
    FriendBoardPostDetailView,
)
from .views.posts.comments import FriendBoardPostsCommentsCreateView
from .views.comments.comments import FriendBoardCommentsCommentsCreateView

# 술친구 urls.py

# app_name을 통해 url namespace를 만들어주고 reverse를 통한 controller name을 만들어준다 
app_name = 'friendboard' 

urlpatterns = [
    path('create/', FriendBoardPostCreateView.as_view(), name="create"),
    path('<int:pk>/delete', FriendBoardPostDeleteView.as_view(), name="delete"),
    path('', FriendBoardPostListView.as_view(), name="list"),
    path('<int:pk>/', FriendBoardPostDetailView.as_view(), name="detail"),
    path('<int:pk>/comments', FriendBoardPostsCommentsCreateView.as_view(), name="createcomment"),
    path('comments/<int:pk>/comments', FriendBoardPostsCommentsCreateView.as_view(), name="createcommentscomment"),
]
