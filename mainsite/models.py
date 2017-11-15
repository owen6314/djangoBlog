from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible


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

    # summary
    excerpt = models.CharField(max_length=200, blank=True)

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    # 待解释：获取post的url， pk是主键
    def get_absolute_url(self):
        return reverse('mainsite:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']
