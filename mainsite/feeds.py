from django.contrib.syndication.views import Feed

from .models import Post


# RSS需要XML文档内容，Feed类可以创建符合该格式的内容
class AllPostsRssFeed(Feed):

    # 显示在聚合阅读器上的标题
    title = "Sky of cloud"

    # 通过聚合阅读器跳转到网站的地址
    link = "localhost6314.com"

    # 显示在阅读器上的描述信息
    description = "Owen's blog"

    # 需要显示的内容条目
    def items(self):
    	return Post.objects.all()

    # 阅读器中显示的内容条目的标题
    def item_title(self, item):
    	return '[%s] %s' % (item.category, item.title)

    # 阅读器中显示的内容的描述
    def item_description(self, item):
    	return item.body