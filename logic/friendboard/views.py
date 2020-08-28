from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from friendboard.models import Post, Comment
from friendboard.forms import PostForm, CommentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView
import logging
# 술친구 views.py

class FriendBoardList(ListView):
    model = Post
    paginate_by = 5
    # context_object_name = "post_list" # default는 object_list, paginate 적용시 page_obj도 가능
    # 생략되어 있음 template_name = 'friendboard/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = context.pop('page_obj', [])
        return context

class FriendBoardCreateView(CreateView):
    model = Post
    fields = ['content', 'password']
    success_url = reverse_lazy('friendboard:list')
    
    def form_valid(self, form):
        super().form_valid(form)
        messages.info(self.request, "친구 찾기를 시작했습니다.")
        return HttpResponseRedirect(self.get_success_url())

class FriendBoardDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('friendboard:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        valpw = request.POST['valpw']

        if self.object.password == valpw:
            self.object.delete()
            messages.info(request, '게시물 삭제에 성공했습니다.')
        else:
            messages.error(request, '패스워드가 다릅니다.')

        return HttpResponseRedirect(self.get_success_url())

class FriendBoardDetail(DetailView):
    model = Post.objects.all()
    context_object_name = "post_list"
    paginate_by = 10
    template_name = 'friendboard.html'

    def get_context_data(self, **kwargs):
        paginator = Paginator(
            super().get_queryset(), 
            self.paginate_by)
        page = self.request.GET.get('page')
        return {self.context_object_name: paginator.get_page(page)}

def detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    form = CommentForm()
    return render(request, 'friendboardDetail.html', {'post':post, 'form':form})


def createcomment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('friendboard:detail', pk=post.pk)
    else:
        raise Http404("Wrong Access")