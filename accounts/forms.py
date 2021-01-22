from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='必須 有効なメールアドレスを入力してください。',
        label='Eメールアドレス'
    )
    postal_code = forms.IntegerField(
        help_text='必須 "-"を除いた数字だけを入力してください',
        label='郵便番号'
    )
    #郵便番号からの住所検索API（例）郵便番号「7830060」で検索する場合
    #https://zipcloud.ibsnet.co.jp/api/search?zipcode=7830060




    class Meta:
        model = User
        fields = ('username', 'email', 'postal_code', 'password1', 'password2', )
