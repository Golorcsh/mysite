from django.contrib import admin
from .models import BlogType, Blog
# Register your models here.


class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')
admin.site.register(BlogType, BlogTypeAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'blog_type', 'author',  'get_read_num', 'create_date', 'last_updated_time')
admin.site.register(Blog, BlogAdmin)

# class ReadNumAdmin(admin.ModelAdmin):
#     list_display = ['read_num', 'blog']




# admin.site.register(ReadNum, ReadNumAdmin)
