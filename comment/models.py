from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.DO_NOTHING)

    root = models.ForeignKey('self', null=True, related_name='root_comment', on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self', null=True, related_name='parent_comment', on_delete=models.DO_NOTHING)
    reply_to = models.ForeignKey(User, null=True, related_name='replies', on_delete=models.DO_NOTHING,)

    def __str__(self):
        return '%s_%s' %(self.object_id, self.text)

    class Meta:
        ordering = ['comment_time']


# class Replay(models.Model):
    # comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING)
