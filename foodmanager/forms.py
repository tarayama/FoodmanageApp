from django import forms
from datetime import date, timedelta
from .models import FoodCategory, Foodmanager

class FoodForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def method(self):
        name = forms.CharField(
            max_length=256,
            label='商品名')

        category = forms.ModelChoiceField(
            FoodCategory.objects.filter(
                user=self.user),
                label='カテゴリー',
                empty_label='選択してください')

        memo = forms.TextField(
            default='',
            label='詳細')

        limit = forms.DateField(
            default=(date.today()+timedelta(days=1))) #賞味期限 defaultは翌日

    class Meta:
        model = Foodmanager
        fields = ('name', 'category', 'memo', 'limit',)

