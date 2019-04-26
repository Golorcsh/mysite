from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm


def index(request):
    return render(request, 'index.html')


def login(request):
    # username = request.POST.get('username', '')
    # password = request.POST.get('password', '')
    # user = auth.authenticate(request, username=username, password=password)
    # # 获得引用的页面
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    # if user is not None:
    #     auth.login(request, user)
    #     return redirect(referer)
    # else:
    #     return render(request, 'login.html', {'message': '用户名或密码错误', 'redirect_to': referer })
    content = {}
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    content['login_form'] = login_form
    return render(request, 'login.html', content)


def register(request):
    content = {}
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 注册
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # 登陆
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        register_form = RegisterForm()
    content['register_form'] = register_form
    return render(request, 'register.html', content)


def logout(request):
    auth.logout(request)
    return redirect(reverse('home'))