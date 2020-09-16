from django.shortcuts import redirect, reverse
from rest_framework.response import Response
from rest_framework import status
from lostboard.views.base_view import BaseView
from lostboard.paginators.posts import PostsPaginator
from lostboard.services.password_validation_service import PasswordValidationService
class PostsView(BaseView):
    pagination_class = PostsPaginator

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)

        if request.accepted_renderer.format == 'html':
            return redirect(
                reverse('lostboard:posts-detail', kwargs={'pk': instance.pk})
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        found = self.get_object().found

        if PasswordValidationService(
            request_password=request.POST.get('password', ""),
            instance_password=self.get_object().password
        ).call():
            json_response = super().destroy(request, *args, **kwargs)
        else:
            json_response = Response({'password': "is not correct"}, status=status.HTTP_400_BAD_REQUEST)

        if request.accepted_renderer.format == 'html':
            return redirect("%s?found=%s" % (
                reverse('lostboard:posts-list'), found
            ))
        return json_response

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            found = self.request.GET.get('found', True)
            if found == 'False': found=False
            return queryset.filter(found=found)
        else:
            return queryset.all()
