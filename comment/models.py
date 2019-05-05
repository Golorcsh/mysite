import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

# Create your models here.


class Sendmail(threading.Thread):

    def __init__(self, subject, text, email, fail_silently):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, self.text, settings.EMAIL_HOST_USER, [self.email], fail_silently=self.fail_silently)


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    root = models.ForeignKey('self', null=True, related_name='root_comment', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, related_name='parent_comment', on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, null=True, related_name='replies', on_delete=models.CASCADE,)

    def __str__(self):
        return '%s_%s' %(self.object_id, self.text)

    def send_mail(self):
        # 发送邮件通知
        content ={}
        if self.parent is None:
            # 评论博客
            subject = '有人评论了你的博客'
            email = self.content_object.get_email()
        else:
            # 回复评论
            subject = '有人回复了你的评论'
            email = self.reply_to.email
        if email != '':
            content['comment_text'] = self.text
            content['url'] = self.content_object.get_url()
            text = render_to_string('send_email.html', content)
            send_mail = Sendmail(subject, text, email, False)
            send_mail.start()

    class Meta:
        ordering = ['comment_time']



