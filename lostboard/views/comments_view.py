from django.shortcuts import redirect, reverse, get_object_or_404
from lostboard.views import BaseView
from lostboard.models import Comment
from lostboard.services.posts_comments_deactive_service import PostsCommentsDeactiveService

class CommentsView(BaseView):
    def list(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        pass

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        PostsCommentsDeactiveService(instance=comment).call()
        return redirect(reverse('lostboard:posts-detail', kwargs={'pk': comment.post.pk}))
