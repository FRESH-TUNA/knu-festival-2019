from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from friendboard.models import Post, Comment
from friendboard.forms import PostForm, CommentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView

class FriendBoardCommentsCommentsCreateView(CreateView):
    form_class = CommentForm
    model = Comment
    # fields = ['content', 'password']
    
    def get_success_url(self):
        return reverse_lazy('friendboard:detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        parent_comment = self.model.objects.get(pk=self.kwargs['pk'])
        form = self.get_form_class()(self.request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.parent = parent_comment
            comment.depth = parent_comment.depth + 1
            comment.post = parent_comment.post
            comment.save()
            messages.info(self.request, "댓글 작성에 성공했습니다.")
            return HttpResponseRedirect(self.get_success_url())
        else:
            raise Http404("Wrong Access")