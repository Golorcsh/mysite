from django.contrib import admin
from picture.models import Picture
# Register your models here.


class PictureAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'create_date']
admin.site.register(Picture,PictureAdmin)