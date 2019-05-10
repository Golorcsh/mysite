from django.db import models

# Create your models here.


class Picture(models.Model):
    title = models.CharField(default='title', max_length=50)
    description = models.TextField(default='description', max_length=200)
    image = models.ImageField(default='default.jpg', upload_to='picture_image/')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<picture_%s> %s' %(self.id, self.title)

    class Meta:
        ordering = ['-create_date']