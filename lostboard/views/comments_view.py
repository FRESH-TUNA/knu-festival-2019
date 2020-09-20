from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib import messages
from lostboard.views import BaseView
from lostboard.services.posts_comments_deactive_service import PostsCommentsDeactiveService
from lostboard.services.password_validation_service import PasswordValidationService
from rest_framework.response import Response
from rest_framework import status

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
        delete_success = False

        password_correct = PasswordValidationService(
            request_password=request.POST.get('password', ""),
            instance_password=comment.password
        ).call()
    
        if password_correct:
            PostsCommentsDeactiveService(instance=comment).call()
            delete_success = True
            json_response = Response(status=status.HTTP_204_NO_CONTENT)
        else:
            json_response = Response({'password': "is not correct"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.accepted_renderer.format == 'html':
            if delete_success:
                messages.info(request, '댓글 삭제에 성공했습니다.')
            else:
                messages.error(request, '패스워드가 다릅니다.')
            return redirect(request.META['HTTP_REFERER'])
        else:
            return json_response
