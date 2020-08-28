from django.urls import path
from . import views
from .views import (
    FriendBoardList, 
    FriendBoardCreateView, 
    FriendBoardDeleteView
)

# 술친구 urls.py
app_name = 'friendboard'
urlpatterns = [
    path('create/', FriendBoardCreateView.as_view(), name="create"),
    path('<int:pk>/delete', FriendBoardDeleteView.as_view(), name="delete"),
    path('', FriendBoardList.as_view(), name="list"),
    path('<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/createcomment/', views.createcomment, name="createcomment"),
]