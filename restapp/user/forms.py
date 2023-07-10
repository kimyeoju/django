# from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import User
from django.contrib.auth import get_user_model
# get_user_model은 settings.py AUTH_USER_MODEL = 'user.User'설정했기 때문

User = get_user_model()


class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        # fields는 사용자에게 입력 받을 항목 (폼)
        fields = ['email']
        # fields = UserCreationForm.Meta.fields + ('email',)
        # 필수 부분을 + email까지 해줄 것이다.

class LoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = ['email', 'password']
        # widgets = {
        #     'email': forms.EmailInput(attrs={'placeholder': 'email'}),
        #     'password': forms.PasswordInput(attrs={'placeholder': 'password'}),
        # }