from rest_framework.response import Response
from rest_framework import status
from lostboard.models import Post

class ListModelMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CreateModelMixin:   
    def create(self, request, *args, **kwargs):
        self.perform_create()
        return Response(
            {
                "is_like": True,
                "count": CommentLike.objects.all().filter(
                    comment=Comment.objects.get(id=self.kwargs["comment_pk"])
                ).count()
            }, status=status.HTTP_201_CREATED
        )
    
    def perform_create(self):
        CommentLike.objects.create(
            user=self.request.user, comment=Comment.objects.get(id=self.kwargs["comment_pk"]))

class DestroyModelMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "is_like": False,
                "count": CommentLike.objects.all().filter(
                    comment=Comment.objects.get(id=self.kwargs["comment_pk"]),
                    like=True
                ).count()
            }, status=status.HTTP_200_OK
        )

    def perform_destroy(self, instance):
        instance.delete()     
