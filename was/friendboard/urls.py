from django.urls import path
from . import views
from .views import FriendBoardList

# 술친구 urls.py
app_name = 'friendboard'
urlpatterns = [
    path('create/', views.post_create, name="create"),
    path('<int:pk>/delete', views.post_delete, name="delete"),
    path('', FriendBoardList.as_view(), name="friendboard"),
    path('<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/createcomment/', views.createcomment, name="createcomment"),
]