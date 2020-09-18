from django.shortcuts import redirect, reverse, get_object_or_404
from lostboard.views import BaseView
from lostboard.models import Comment

class CommentsView(BaseView):
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parent_comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        comment = serializer.save(
            post=parent_comment.post, 
            parent=parent_comment,
            depth=parent_comment.depth + 1
        )
        headers = self.get_success_headers(serializer.data)
        return redirect(reverse('lostboard:posts-detail', kwargs={'pk': comment.post.pk}))

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return redirect('lostboard:posts-list')