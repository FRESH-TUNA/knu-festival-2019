from django.shortcuts import redirect, reverse, get_object_or_404
from lostboard.views import BaseView
from lostboard.models import Comment
from lostboard.services.posts_comments_deactive_service import PostsCommentsDeactiveService
from lostboard.services.password_validation_service import PasswordValidationService

class CommentsView(BaseView):
    def get_queryset(self):
        parent_comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        return self.model.objects.filter(parent=parent_comment)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parent_comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        comment = serializer.save(
            active=True,
            post=parent_comment.post, 
            parent=parent_comment,
            depth=parent_comment.depth + 1
        )
        headers = self.get_success_headers(serializer.data)

        if request.accepted_renderer.format == 'html':
            return redirect(reverse('lostboard:posts-detail', kwargs={'pk': comment.post.pk}))
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
