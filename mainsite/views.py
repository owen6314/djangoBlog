import markdown

from django.shortcuts import render, get_object_or_404

from .models import Post, Category
from comments.forms import CommentForm
# 改成类视图
from django.views.generic import ListView

# 主页视图
class IndexView(ListView):
    # 在这个listview里面，用到的模型是Post
    model = Post
    template_name = 'mainsite/index.html'
    # post_list 这个变量名会被传给模板
    context_object_name = 'post_list'


# 文章详情页面,使用markdown支持语法高亮
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 增加阅读量
    post.increase_views()

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
class ArchivesView(ListView):
    model = Post
    template_name = 'mainsite/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year, created_time__month=month)


# 显示分类页面
class CategoryView(ListView):
    model = Post
    template_name = 'mainsite/index.html'
    context_object_name = 'post_list'

    # 复写父类的get_queryset方法，默认获得模型的全部列表数据
    def get_queryset(self):
        # kwargs是从URL捕获的命名组参数值
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

