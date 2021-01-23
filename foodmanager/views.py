from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FoodCategory, Foodmanager
from django.http import Http404, HttpResponse
from .forms import FoodForm
import json
import requests
import foodmanager.tesseract
import foodmanager.foodbank
import foodmanager.jancode
import numpy as np
from django.views.decorators.csrf import csrf_exempt

#ログイン前トップ
def index(request):
    if request.user.is_authenticated:
        return redirect('top')
    return render(request, 'foodmanager/index.html', {})

#ログイン後トップ
@login_required
def top(request):
    Food_list = Foodmanager.objects.filter(user=request.user)
    category_list = FoodCategory.objects.all()
    context = {
        'Food_list': Food_list,
        'category_list' : category_list
        }
    return render(request, 'foodmanager/top.html',context)

#カテゴリー作成(iOSアプリのため未実装)
def make_category(request):
    category_list = FoodCategory.objects.filter(user=request.user)
    
    if request.method == "POST":
        for category in category_list:
            if category.getName() != request.POST['category']:
                new_category = FoodCategory(
                    user = request.user,
                    name = request.POST['category']
                )
                new_category.save()
                return redirect('#')
    return render(request, 'foodmanager/top.html', {})

#新規食品登録(iOSアプリのため未実装)
def new_Food(request):
    Food_list = Foodmanager.objects.filter(user=request.user)
    category_list = FoodCategory.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = FoodForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_Food = Foodmanager(
                user = request.user,
                name = form.cleaned_data.get['name'],
                category = form.cleaned_data.get['category'],
                memo = form.cleaned_data.get['memo'],
                limit = form.cleaned_data.get['limit']
            )
            new_Food.save()
        else:
            form = FoodForm(user=request.user, data=request.POST)
        return redirect('top', request.user)
    context = {
        'Food_list': Food_list,
        'category_list' : category_list,
        'form' : form
        }
    return render(request, 'foodmanager/new_food.html', {context})

#JANコードからの商品名取得
def jancode_to_productname(request, jancode):
    result = {}
    result['product_name'] = "ヒットしませんでした。手入力してください"
    food = foodmanager.jancode.FoodName(jancode)
    try:
        food.setYahooProductName()
        print(food.getName())
        food.setShorterFoodName()
        print(food.getName())
        result['product_name'] = food.getName()
    except:
        return HttpResponse(json.dumps(result),status=400)
    return HttpResponse(json.dumps(result),status=200)

#賞味期限画像からの賞味期限自体の認識
@csrf_exempt
def Image_to_Limit(request):
    result = {}
    if request.method == 'POST':
        print(request.FILES)
        print(request.FILES['uploadFile'])
        img = request.FILES['uploadFile']
        str_list = foodmanager.tesseract.pytesseract_jpn(img)
        #str_list = foodmanager.tesseract.pyocr_tesseract(img)
        result_list = foodmanager.tesseract.drop_limit(str_list)
        print(result_list)
        result = {"result" : result_list}
        return HttpResponse(json.dumps(result),status=200)
    else:
        result = {"result" : "error occurred. may be mistake method"}
        return HttpResponse(json.dumps(result),status=400)


#郵便番号からの近隣5件のフードバンク検索
def post_to_foodbank(request, postal_code): # 
    df = foodmanager.foodbank.get_near_foodbanks(str(postal_code))
    print(df)
    result = json.loads(df)
    print(type(result))
    result = {"result" : result }
    return HttpResponse(json.dumps(result, cls = foodmanager.foodbank.JsonEncoder),status=200)
   
