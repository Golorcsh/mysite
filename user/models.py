from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    image = models.ImageField(default='default.jpg', upload_to='profile_image/')

    def __str__(self):
        return '<Profile> %s for %s' %(self.nickname, self.user.username)


def get_username_or_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username


def get_profile(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.image.url


User.get_username_or_nickname = get_username_or_nickname
User.get_profile = get_profile
