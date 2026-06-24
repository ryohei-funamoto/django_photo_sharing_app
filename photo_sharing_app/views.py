from django.shortcuts import render, get_object_or_404
from .models import Post

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
