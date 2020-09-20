from django.shortcuts import redirect, reverse, get_object_or_404
from lostboard.views import BaseView
from lostboard.models import Post

class CommentsView(BaseView):
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            post=get_object_or_404(Post, pk=self.kwargs['post_pk']),
            active=True
        )
        headers = self.get_success_headers(serializer.data)

        if request.accepted_renderer.format == 'html':
            return redirect(
                reverse('lostboard:posts-detail', kwargs={'pk': self.kwargs['post_pk']})
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
