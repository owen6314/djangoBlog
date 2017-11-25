from django.db import models
from django.utils.six import python_2_unicode_compatible


# 该装饰器用于兼容python2
@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=100)
    # email = models.EmailField(max_length=255)
    # url = models.URLField(blank=True)
    text = models.TextField()
    # 当评论数据加载到数据库时，自动把时间设置为当前时间
    create_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('mainsite.Post')

    def __str__(self):
        return self.text[:20]
