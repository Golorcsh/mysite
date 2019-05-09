from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='用户名', widget=forms.TextInput(
        attrs={'autocomplete': "off", 'placeholder': '请输入用户名或邮箱'}))

    password = forms.CharField(label='密码', widget=forms.PasswordInput(
        attrs={'placeholder': '请输入密码'}))

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名/邮箱或密码不正确')
        else:
            self.cleaned_data['user'] = user

        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20, min_length=6, widget=forms.TextInput(
        attrs={'autocomplete': "off", 'placeholder': '请输入用户名(6-20)'}))

    email = forms.EmailField(label='邮箱', required=False, widget=forms.TextInput(
        attrs={'placeholder': '请输入邮箱'}))

    verification_code = forms.CharField(label='验证码', required=False, widget=forms.TextInput(
            attrs={'autocomplete': "off", 'placeholder': '点击“发送验证码”发送到邮箱'}))

    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(
        attrs={'placeholder': '请输入密码'}))

    password_again = forms.CharField(label='确认密码', min_length=6, widget=forms.PasswordInput(
        attrs={'placeholder': '请再输入密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email= self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError("两次输入密码不一致，请重新输入密码")
        return password_again

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')

        code = self.request.session.get('register_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return verification_code


class ChangeNickname(forms.Form):
    nickname = forms.CharField(label='新昵称', required=False, max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': "off", 'placeholder': '请输入昵称'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNickname, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname', '').strip()
        if nickname == '':
            raise forms.ValidationError("昵称不能为空")
        return nickname


class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder':'请输入正确的邮箱'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autocomplete': "off", 'placeholder': '点击“发送验证码”发送到邮箱'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')

        # 判断用户是否已绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')

        # 判断验证码
        code = self.request.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经被绑定')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code


class ChangePasswordForm(forms.Form):
    password_old = forms.CharField(label='原密码', min_length=6, widget=forms.PasswordInput(
        attrs={'placeholder': '请输入原密码'}))

    password_new = forms.CharField(label='新密码', min_length=6, widget=forms.PasswordInput(
        attrs={'placeholder': '请输入新密码'}))

    password_again = forms.CharField(label='确认密码', min_length=6, widget=forms.PasswordInput(
        attrs={'placeholder': '请再输入密码'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        password_new = self.cleaned_data.get('password_new', '')
        password_again = self.cleaned_data.get('password_again', '')

        if password_again != password_new or password_new == '':
            raise forms.ValidationError('两次输入密码不一致，请重新输入密码')
        return self.cleaned_data

    def clean_password_old(self):
        password_old = self.cleaned_data.get('password_old', '')
        if not self.user.check_password(password_old):
            raise forms.ValidationError('原密码错误')
        return password_old


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='邮箱', required=False, widget=forms.TextInput(
        attrs={'placeholder': '请输入账号绑定的邮箱'}))

    verification_code = forms.CharField(label='验证码', required=False, widget=forms.TextInput(
                attrs={'autocomplete': "off", 'placeholder': '点击“发送验证码”发送到邮箱'})
    )
    password_new = forms.CharField(label='新密码', min_length=6, widget=forms.PasswordInput(
        attrs={'placeholder': '请输入新密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('用户为绑定邮箱')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')

        code = self.request.session.get('forgot_password_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return verification_code