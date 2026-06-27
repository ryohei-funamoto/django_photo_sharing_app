from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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
