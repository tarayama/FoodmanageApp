from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FoodCategory, Foodmanager
from django.http import Http404, HttpResponse
from .forms import FoodForm
import json
import requests
import foodmanager.tesseract
import foodmanager.foodbank
import numpy as np
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    #ログイン前トップ
    if request.user.is_authenticated:
        return redirect('top')
    return render(request, 'foodmanager/index.html', {})

@login_required
def top(request):
    #ログイン後トップ
    Food_list = Foodmanager.objects.filter(user=request.user)
    #for food in Food_list:
    #    print(food)
    #print(Food_list)
    category_list = FoodCategory.objects.all()
    context = {
        'Food_list': Food_list,
        'category_list' : category_list
        }
    return render(request, 'foodmanager/top.html',context)



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

def jancode_to_productname(request, jancode):
    result = {}
    result['product_name'] = "ヒットしませんでした。手入力してください"
    if jancode != 0:
        print("jancodeを取得しました")
    yahoo_client_id = 'dj00aiZpPWFzd2tQN1NCUG1HbSZzPWNvbnN1bWVyc2VjcmV0Jng9ZWQ-' #yahoo! network service
    #code = '4902102072618' test用(coca-cola)
    baseurl = "http://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"
    params = {
        'appid' : yahoo_client_id,
        'jan_code' : jancode
    }
    response = requests.get(baseurl, params=params)
    try:
        values = json.loads(response.text)
        result['product_name'] = values.get("hits")[0].get("name")
        result ['parent_category_name'] = values.get("hits")[0].get("parentGenreCategories")
        result['category_name'] = values.get("hits")[0].get("genreCategory").get("name")
        result['description'] = values.get("hits")[0].get("description")
        
    except:
        return HttpResponse(json.dumps(result),status=400)
    return HttpResponse(json.dumps(result),status=200)

@csrf_exempt
def Image_to_Limit(request):
    result = {}
    #try:
    if request.method == 'POST':
        print(request.FILES)
        print(request.FILES['uploadFile'])
        img = request.FILES['uploadFile']
        #try:
        str_list = foodmanager.tesseract.pytesseract_jpn(img)
        #except:
        #    str_list = foodmanager.tesseract.pyocr_tesseract(img)
        result_list = foodmanager.tesseract.drop_limit(str_list)
        print(result_list)
        result = {"result" : result_list}
        return HttpResponse(json.dumps(result),status=200)
    else:
        result = {"result" : "error occurred. may be mistake method"}
        return HttpResponse(json.dumps(result),status=400)
    
   # except:
    #    result = {"result" : "error occurred. failed to get image or failed to read limit"}
    #    return HttpResponse(json.dumps(result),status=400)

def post_to_foodbank(request, postal_code): # 
    #result = {}

    df = foodmanager.foodbank.get_near_foodbanks(str(postal_code))
    print(df)
    result = json.loads(df)
    print(type(result))
    result = {"result" : result }
    return HttpResponse(json.dumps(result, cls = foodmanager.foodbank.JsonEncoder),status=200)
        
    #except:
    #    result = {"result" : "error occurred"}
    #    return HttpResponse(json.dumps(result),status=400)
