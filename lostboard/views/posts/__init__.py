from django.shortcuts import redirect
from lostboard.views import BaseGenericViewSet
from lostboard.paginators.posts import PostsPaginator
from lostboard.mixins.posts import CreateModelMixin
from lostboard.models import Post
import logging

class PostsViewSet(CreateModelMixin, BaseGenericViewSet):
    pagination_class = PostsPaginator
    model = Post

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return redirect('lostboard:posts-list')

    def get_queryset(self):
        if self.action == 'list':
            found = self.request.GET.get('found', True)
            if found == 'False': found=False
            return self.model.objects.filter(found=found)
        else:
            return self.model.objects.all()
