from django.urls import path
from rest_framework import routers
from rest_framework import generics
from . import views
from django.contrib.auth.models import User
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('GET/userinfo/', csrf_exempt(UserList.as_view())),
    
    #Category API
    path('GET/Category/', csrf_exempt(CategoryList.as_view())),
    path('POST/Category/create', csrf_exempt(CategoryCreate.as_view())),
    path('GET/Category/retrieve/<int:pk>', csrf_exempt(CategoryRetrieve.as_view())),
    path('PUT/Category/retrieve_update/<int:pk>', csrf_exempt(CategoryRetrieveUpdate.as_view())),
    path('PUT/Category/Update/<int:pk>', csrf_exempt(CategoryUpdate.as_view())),
    path('DELETE/Category/<int:pk>', csrf_exempt(CategoryDestroy.as_view())),
    #Food API
    path('GET/Food/', csrf_exempt(FoodList.as_view())),
    path('POST/Food/create', csrf_exempt(FoodCreate.as_view())),
    path('GET/Food/retrieve/<int:pk>', csrf_exempt(FoodRetrieve.as_view())),
    path('PUT/Food/retrieve_update/<int:pk>', csrf_exempt(FoodRetrieveUpdate.as_view())),
    path('PUT/Food/Update/<int:pk>', csrf_exempt(FoodUpdate.as_view())),
    path('DELETE/Food/<int:pk>', csrf_exempt(FoodDestroy.as_view())),
]
