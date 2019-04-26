from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse


def index(request):
    return render(request, 'index.html')


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    # 获得引用的页面
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message': '用户名或密码错误', 'redirect_to': referer })