from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadExpandMethod, ReadDetail


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadExpandMethod):  # 继承
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)  # 反向关联ReadDetail模型(模型里要有content_type字段)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return'<Blog: %s>' % self.title

    def get_url(self):
        # 返回评论页面链接
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        # 获取email
        return self.author.email

    class Meta:
        ordering = ['-created_time']  # 设置默认排序

