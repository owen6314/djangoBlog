from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
import markdown
from django.utils.html import strip_tags


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 摘要
    excerpt = models.CharField(max_length=200, blank=True)

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    author = models.ForeignKey(User)

    # 阅读量
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    # 待解释：获取post的url， pk是主键
    def get_absolute_url(self):
        return reverse('mainsite:detail', kwargs={'pk': self.pk})

    # 访问量加1，update_fields = ['views']可以提高效率
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 复写save方法，使得如果摘要为空，则自动取body的前50个字符作为摘要
    def save(self, *args, **kwargs):
        if not self.excerpt:
            # 实例化一个Markdown类，渲染body文本
            md = markdown.Markdown(extensions = [
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                ])
            # 将markdown渲染成html文本
            # strip_tags去掉html标签，再截取前50个字符
            self.excerpt = strip_tags(md.convert(self.body))[:50]

        # 调用父类save方法
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']
