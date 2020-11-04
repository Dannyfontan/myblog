from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone
from mdeditor.fields import MDTextField
# Create your models here.

class ArticleColumn(models.Model):
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    body = MDTextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-updated',)
    
    def __str__(self):
        return self.title