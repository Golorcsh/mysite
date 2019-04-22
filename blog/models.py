from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
import ckeditor
# Create your models here.


class BlogType(models.Model):
    type_name = models.CharField(default='Blog_type', max_length=50)

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(default='title', max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_date = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-create_date']