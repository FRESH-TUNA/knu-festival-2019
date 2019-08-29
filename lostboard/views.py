from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.exceptions import PermissionDenied
from .models import Post, Comment
from .forms import PostForm, CommentForm
from . import urls

# 분실물 views.py

def board(request, found='found'):
    if found == 'found':
        lostposts = Post.objects.filter(found=True).order_by('-created_at')
    else:
        lostposts = Post.objects.filter(found=False).order_by('-created_at')
    form = PostForm()
    return render(request,'lostboard.html', {'lostposts':lostposts, 'form':form})

def createpost(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            lostpost = form.save(commit=False)
            lostpost.password = form.cleaned_data['password']
            lostpost.save()
        else:
            print(form.errors)
            raise Http404("form is not valid")
        return redirect('lostboard:detail', lostpost.pk)
    else:
        raise Http404("Wrong Access")

def detail(request, pk):
    try:
        lostpost = Post.objects.get(pk=pk)
    except LostPost.DoesNotExist:
        raise Http404("Post does not exist")
    form = CommentForm()
    return render(request, 'lostdetail.html', {'lostpost':lostpost, 'form':form})

def createcomment(request, pk):
    lostpost = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.lostpost = lostpost
            comment.save()
            return redirect('lostboard:detail', pk=lostpost.pk)
    else:
        raise Http404("Wrong Access")

def deletepost(request, pk):
    try:
        lostpost = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    if request.method == 'POST':
        if request.POST['password'] == lostpost.password:
            lostpost.delete()
            return redirect('lostboard:board')
        raise PermissionDenied("Password is not matched")
    else:
        path = urls.app_name + ":deletepost"
        return render(request, 'lostpwcheck.html', {'lostpost': lostpost, 'path':path})
    