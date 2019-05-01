from django.contrib import admin
from .models import Comment
# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',  'parent', 'comment_time', 'content_object', 'text')
admin.site.register(Comment, CommentAdmin)