from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-created_at')

    context = {
        'posts': posts,
    }

    return render(
        request,
        'photo_sharing_app/index.html',
        context=context,
    )

def show(request, id):
    post = get_object_or_404(Post, pk=id)

    context = {
        'post': post,
    }

    return render(
        request,
        'photo_sharing_app/detail.html',
        context=context,
    )

@login_required
def create(request):
    form = PostForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.posted_by = request.user
        post.save()
        return redirect('photo_sharing_app:index')

    context = {
        'form': form,
    }

    return render(
        request,
        'photo_sharing_app/create.html',
        context=context,
    )

@login_required
def edit(request, id):
    post = get_object_or_404(Post, pk=id)

    form = PostForm(request.POST or None, instance=post)

    if post.posted_by == request.user:
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('photo_sharing_app:show', id=post.id)
    else:
        raise PermissionDenied

    context = {
        'post': post,
        'form': form,
    }

    return render(
        request,
        'photo_sharing_app/edit.html',
        context=context,
    )

@login_required
def delete(request, id):
    post = get_object_or_404(Post, pk=id)

    if request.user == post.posted_by:
        if request.method == 'POST':
            post.delete()
            return redirect('photo_sharing_app:index')
        else:
            return redirect('photo_sharing_app:show', id=post.id)
    else:
        raise PermissionDenied
