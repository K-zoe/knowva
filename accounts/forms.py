from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username':forms.TextInput(
                attrs = {'placeholder':'20文字以内で入力してください。'}
            ),
            'email':forms.EmailInput(
                attrs = {'placeholder':''}
            ),
        }

class LoginForm(AuthenticationForm):
    #emailでログインするが継承元の制約のため変数名はusernameのままにする。
    username = forms.EmailField(
        required = True,
        widget = forms.EmailInput(attrs={'autofocus': True})
    )
    error_messages ={
        'invalid_login':'メールアドレスかパスワードに<br>誤りがあります。',
        'is_active':'このユーザーは退会しています。<br>復活するには管理者にお問い合わせください。',
        'is_banned':'このユーザーは凍結されています。<br>解除については管理者にお問い合わせください。'
    }

    def confirm_login_allowed(self, user):
        if user.is_banned:
            raise ValidationError(
                self.error_messages['is_banned'],
                code = 'is_banned'
            )
        
        if not user.is_active:
            raise ValidationError(
                self.error_messages['is_active'],
                code = 'is_active'
            )