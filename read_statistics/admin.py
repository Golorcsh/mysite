from django.contrib import admin
from read_statistics.models import ReadNum
# Register your models here.


class ReadNumAdmin(admin.ModelAdmin):
    list_display = ( 'content_object', 'read_num',)
admin.site.register(ReadNum, ReadNumAdmin)



