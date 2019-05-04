from .models import Comment
from .forms import CommentForm
from django.urls import reverse
from django.http import JsonResponse
# Create your views here.


def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    data = {}
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        # 判断是否为回复
        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.parent = parent
            comment.reply_to = parent.user
            comment.root = parent if parent.root is None else parent.root
        comment.save()

        # 发送邮件通知
        comment.send_mail()

        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_username_or_nickname()
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text

        if parent is not None:
            data['reply_to'] = comment.reply_to.get_username_or_nickname()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root is not None else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]

    return JsonResponse(data)


