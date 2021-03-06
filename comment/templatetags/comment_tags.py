from django import template
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from ..forms import CommentForm
from ..models import Comment


EachPageNumOfComment = 10

# 自定义模板标签
register = template.Library()
@register.simple_tag
def get_comment_num(obj):
    # 获取评论对象的类型
    content_type = ContentType.objects.get_for_model(obj)
    comment_num = Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()
    return comment_num


@register.simple_tag
def get_comment_form(obj):
    # 获取评论对象的类型
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={'content_type': content_type.model, 'object_id': obj.pk, 'reply_comment_id': 0})
    return form


@register.simple_tag
def get_comment(obj):
    # 获取评论对象的类型
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None).order_by('-comment_time')
    return comments

