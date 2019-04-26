from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
# Create your views here.


def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    user = request.user
    text = request.POST.get('text', '').strip()
    
    # 检查数据
    if text == '':
        return render(request, 'error.html', {'message': "评论不不能为空" ,'redirect_to': referer})
    
    try:
        # 获取了blog类型的字符串变量需要处理
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        # 处理blog字符串变成一个类
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message': "评论对象不存在", 'redirect_to': referer})
    
    # 保存数据
    comment = Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    
    
    return redirect(referer)



