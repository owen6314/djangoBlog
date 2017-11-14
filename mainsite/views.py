import markdown
from django.shortcuts import render, get_object_or_404
from .models import Post


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'mainsite/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body, extensions=[
                                  'markdown.extensions.extra',
                                  'markdown.extensions.codehilite',
                                  'markdown.extensions.toc'])
    return render(request, 'mainsite/detail.html', context={'post': post})
