from django.shortcuts import render, get_object_or_404, redirect
from mainsite.models import Post

from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        # 用户提交的数据存在request.POST中，是一个类字典对象
        form = CommentForm(request.POST)
        if form.is_valid():
            # commit=False意思是，仅仅利用表单的数据生成Comment模型类的实例，暂不将其保存到数据库
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            # redirect接受一个模型的实例时，会调用这个模型实例的get_absolute_url方法，重定向到返回的url
            return redirect(post)
    else:
        # TODO:返回评论错误信息
        # 作用等价于post.objects.filter(post=post)，关联模型小写加_set返回一个类似objects的manager
        comment_list = post.comment_set.all()
        context = {'post': post, 'form': form, 'comment_list': comment_list}
        return render(request, 'mainsite/detail.html', context=context)

    # 不是post请求，再返回文章页面
    return redirect(post)
