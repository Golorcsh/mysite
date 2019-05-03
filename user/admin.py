from django.contrib import admin
from user.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')
admin.site.register(Profile, ProfileAdmin)