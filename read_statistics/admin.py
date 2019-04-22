from django.contrib import admin
from read_statistics.models import ReadNum
# Register your models here.


class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object')
admin.site.register(ReadNum, ReadNumAdmin)