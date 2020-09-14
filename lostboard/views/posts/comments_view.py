from django.shortcuts import redirect, reverse, get_object_or_404
from lostboard.views import BaseGenericViewSet
from lostboard.mixins.posts import CreateModelMixin
from lostboard.models import Post

class CommentsView(BaseGenericViewSet):
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(lostpost=get_object_or_404(Post, pk=self.kwargs['post_pk']))
        headers = self.get_success_headers(serializer.data)
        return redirect(reverse('lostboard:posts-detail', pk=self.kwargs['post_pk']))


    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return redirect('lostboard:posts-list')
