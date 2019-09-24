from django.shortcuts import render, redirect, get_object_or_404
from friendboard.models import Post, Comment
from friendboard.forms import PostForm, CommentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.views.generic import ListView, DetailView
import logging
# 술친구 views.py

class FriendBoardList(ListView):
    queryset = Post.objects.all()
    context_object_name = "post_list"
    paginate_by = 10
    template_name = 'friendboard.html'

    def get_context_data(self, **kwargs):
        paginator = Paginator(
            super().get_queryset(), 
            self.paginate_by)
        page = self.request.GET.get('page')
        return {self.context_object_name: paginator.get_page(page)}

## function_based_view
# def friendboard(request):
#     post_list = Post.objects.all()
#     paginator = Paginator(post_list, 10) # Show 25 contacts per page
#     page = request.GET.get('page')
#     post_list = paginator.get_page(page)
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/friendboard/')
#     else:
#         form = PostForm()
#     return render(request,'friendboard.html',{'post_list':post_list,'form':form})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/friendboard/')
    else:
        form = PostForm()
    return render(request, 'friendboard.html',{'forms':forms})

def post_delete(request, pk):
    valpw = request.POST['valpw']
    post = Post.objects.get(pk=pk)
    if post.password == valpw :
        post.delete()
        messages.info(request, '게시물 삭제에 성공했습니다.')
    else :
        messages.error(request, '패스워드가 다릅니다.')
    return redirect('/friendboard/')


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