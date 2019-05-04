import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.conf import  settings
from django.core.mail import send_mail
from user.forms import LoginForm, RegisterForm, ChangeNickname, BindEmailForm, ChangePasswordForm, ForgotPasswordForm
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
        register_form = RegisterForm(request.POST ,request=request)
        if register_form.is_valid():
            # 注册
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # 清理session
            del request.session['register_code']
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


def change_password(request):
    redirect_to = request.GET.get('from', reverse('home'))
    content = {}
    if request.method == 'POST':
        forgot_password_form = ChangePasswordForm(request.POST, user=request.user)
        if forgot_password_form.is_valid():
            user = request.user
            password_new = forgot_password_form.cleaned_data['password_new']
            user.set_password(password_new)
            user.save()
            auth.logout(request)
            return redirect(reverse('login'))
    else:
        change_password_form = ChangePasswordForm()

    content['form'] = change_password_form
    content['page_title'] = '修改密码'
    content['form_title'] = "修改密码"
    content['submit_text'] = '修改'
    content['return_back_url'] = redirect_to
    return render(request, 'user/change_password.html', content)


def forgot_password(request):
    redirect_to = reverse('home')
    context = {}
    if request.method == 'POST':
        forgot_password_form = ForgotPasswordForm(request.POST, request=request)
        if forgot_password_form.is_valid():
            email = forgot_password_form.cleaned_data['email']
            user = User.objects.get(email=email)
            password_new = forgot_password_form.cleaned_data['password_new']
            user.set_password(password_new)
            user.save()
            # 清理session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        forgot_password_form = ForgotPasswordForm()

    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = forgot_password_form
    context['return_back_url'] = redirect_to
    return render(request, 'user/forgot_password.html', context)


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清理session
            del request.session['bind_email_code']
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
    data = {}
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')

    # 生成验证码
    code = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    mail_content = 'http://golor.xyz' + ' verification code:%s' %code

    if email != '':
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now

            # 发送邮件
            send_mail(
                'Golor\'Blog',
                mail_content,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


