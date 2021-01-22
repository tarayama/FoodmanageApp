from django.db import models
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
class FoodCategory(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE)
    name = models.CharField(max_length=256) #カテゴリー 例) 魚類、肉類、野菜など

    def __str__(self):
        return self.name

    def getName(self):
        return self.name

class Foodmanager(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE) #もしユーザーが削除されたらこの食品も削除
    name = models.CharField(max_length=256) #商品名
    memo = models.TextField(default='') #詳細の記入
    category = models.ForeignKey(
        FoodCategory,
        on_delete=models.CASCADE,
        blank=True,
        null=True) #もしカテゴリーが削除されたらこの食品も削除
    limit = models.DateField(default=(date.today()+timedelta(days=1))) #賞味期限 defaultは翌日
    solution = models.IntegerField(default=0) #解決済みか否か 未解決は０

    def __str__(self):
        return self.name
    
    def getName(self):
        return self.name
    
    def getCategoryName(self):
        return self.Category.name

class Barcode(models.Model):
    jancode = models.IntegerField(default=0)
    name = models.CharField(
        default="商品名を取得できませんでした",
        max_length=256,
        blank=True,
        null=True)
    Category = models.CharField(
        default="categoryの名前を取得できませんでした",
        max_length=256,
        blank=True,
        null=True)

    def __str__(self):
        return self.name

#class UsebyDate(models.Model):
#    limitImage = models.ImageField(
#        upload_to='image/'
#    )

    
    
        


