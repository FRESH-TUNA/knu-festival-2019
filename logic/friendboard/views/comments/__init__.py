from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from friendboard.models import Post, Comment
from friendboard.forms import PostForm, CommentForm
from django.contrib import messages
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import DeleteView

class FriendBoardCommentsDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('friendboard:detail', kwargs={'pk': self.get_object().post.pk})

    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        self.object = self.get_object()
        valpw = request.POST['valpw']

        if self.object.password == valpw:
            self.object.delete()
            messages.info(request, '게시물 삭제에 성공했습니다.')
        else:
            messages.error(request, '패스워드가 다릅니다.')

        return HttpResponseRedirect(success_url)