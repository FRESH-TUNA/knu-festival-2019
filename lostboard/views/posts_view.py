from django.shortcuts import redirect, reverse
from lostboard.views import BaseGenericViewSet
from lostboard.paginators.posts import PostsPaginator
import logging

class PostsView(BaseGenericViewSet):
    pagination_class = PostsPaginator
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        json_response = super().create(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return redirect(reverse('lostboard:posts-list'))
        return json_response

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        json_response = super().destroy(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return redirect(reverse('lostboard:posts-list'))
        return json_response

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            found = self.request.GET.get('found', True)
            if found == 'False': found=False
            return queryset.filter(found=found)
        else:
            return queryset.all()
