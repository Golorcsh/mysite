# Generated by Django 2.2 on 2019-05-10 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='image',
            field=models.ImageField(default='default.png', upload_to='picture_image/'),
        ),
    ]