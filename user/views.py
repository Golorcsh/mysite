import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail
from user.forms import LoginForm, RegisterForm, ChangeNickname, BindEmailForm
from .models import Profile


def login(request):
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
    return render(request, 'user/login.html', content)


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
    return render(request, 'user/register.html', content)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    content = {}
    # profile = Profile.objects.get(user=request.user)
    # content['nickname'] = profile.nickname
    return render(request, 'user/user_info.html', content)


def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))
    content = {}
    if request.method == 'POST':
        nickname_form = ChangeNickname(request.POST, user=request.user)
        if nickname_form.is_valid():
            nickname_new = nickname_form.cleaned_data['nickname']
            profile, create = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        nickname_form = ChangeNickname()

    content['form'] = nickname_form
    content['page_title'] = '修改昵称'
    content['form_title'] = "修改昵称"
    content['submit_text'] = '修改'
    content['return_back_url'] = redirect_to
    return render(request, 'user/form.html', content)


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    data = {}

    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data['status'] = 'ERROR'
        else:
            request.session['bind_email_code'] = code
            request.session['send_code_time'] = now

            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码：%s' % code,
                '1045132383@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


