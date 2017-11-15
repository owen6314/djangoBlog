import markdown

from django.shortcuts import render, get_object_or_404

from .models import Post, Category
from comments.forms import CommentForm


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'mainsite/index.html', context={'post_list': post_list})


# 文章详情页面,使用markdown支持语法高亮
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body, extensions=[
                                  'markdown.extensions.extra',
                                  'markdown.extensions.codehilite',
                                  'markdown.extensions.toc'])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'mainsite/detail.html', context=context)


# 显示归档页面，函数的参数列表中使用属性要用双下划线(django要求)
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
    return render(request, 'mainsite/index.html', context={'post_list': post_list})


# 显示分类页面
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'mainsite/index.html', context={'post_list': post_list})
