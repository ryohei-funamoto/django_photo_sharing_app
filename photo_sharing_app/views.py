from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-created_at')

    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
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
    form = PostForm(
        request.POST or None,
        request.FILES or None
    )

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

    old_image = post.image

    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post
    )

    if post.posted_by == request.user:
        if request.method == 'POST' and form.is_valid():
            updated_post = form.save()
            if old_image and old_image.name != 'images/noimage.png' and old_image.name != updated_post.image.name:
                old_image.delete(save=False)
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
            if post.image.name != 'images/noimage.png':
                post.image.delete()
            post.delete()
            return redirect('photo_sharing_app:index')
        else:
            return redirect('photo_sharing_app:show', id=post.id)
    else:
        raise PermissionDenied
