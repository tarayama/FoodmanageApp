from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.http import Http404, HttpResponse
from foodmanager.models import Foodmanager, FoodCategory
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token 
import re 
from .permissions import IsOwnerOrReadOnly
from .serializers import *
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


# User
class UserList(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(username=user.username)

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

# エンドユーザーに全ユーザー情報を渡す必要はないのでいらないと思う
# django adminで管理すればいいと思う


# Category
class CategoryList(generics.ListAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = CategorySerializer

    #def get_queryset(self):
    #    user = self.request.user
    #    return FoodCategory.objects.filter(user=user)

    #@csrf_exempt
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
    

class CategoryCreate(generics.CreateAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieve(generics.RetrieveAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        return FoodCategory.objects.filter(user=user)

    #@csrf_exempt
    def Retrieve(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

class CategoryRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = CategorySerializer
#    lookup_field = 'price'

    def get_queryset(self):
        user = self.request.user
        return FoodCategory.objects.filter(user=user)

    #@csrf_exempt
    def RetrieveUpdate(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

class CategoryUpdate(generics.UpdateAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = CategorySerializer
#    lookup_field = 'price'

    def get_queryset(self):
        user = self.request.user
        return FoodCategory.objects.filter(user=user)

    #@csrf_exempt
    def Update(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

class CategoryDestroy(generics.DestroyAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        return FoodCategory.objects.filter(user=user)

    #@csrf_exempt
    def Destroy(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

# Food
class FoodList(generics.ListAPIView):
    queryset = Foodmanager.objects.all()
    serializer_class = FoodSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Foodmanager.objects.filter(user=user)

    #@csrf_exempt
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = FoodSerializer(queryset, many=True)
        return Response(serializer.data)

class FoodCreate(generics.CreateAPIView):
    queryset = Foodmanager.objects.all()
    serializer_class = FoodSerializer

    def get_queryset(self):
        user = self.request.user
        return Foodmanager.objects.filter(user=user)

    #@csrf_exempt
    def Create(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = FoodSerializer(queryset, many=True)
        return Response(serializer.data)

class FoodRetrieve(generics.RetrieveAPIView):
    queryset = Foodmanager.objects.all()
    serializer_class = FoodSerializer
#    lookup_field = 'user'

    def get_queryset(self):
        user = self.request.user
        return Foodmanager.objects.filter(user=user)

    #@csrf_exempt
    def Retrieve(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = FoodSerializer(queryset, many=True)
        return Response(serializer.data)

class FoodRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Foodmanager.objects.all()
    serializer_class = FoodSerializer
#    lookup_field = 'price'

    def get_queryset(self):
        user = self.request.user
        return Foodmanager.objects.filter(user=user)

    #@csrf_exempt
    def RetrieveUpdate(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = FoodSerializer(queryset, many=True)
        return Response(serializer.data)

class FoodUpdate(generics.UpdateAPIView):
    queryset = Foodmanager.objects.all()
    serializer_class = FoodSerializer
#    lookup_field = 'price'

    def get_queryset(self):
        user = self.request.user
        return Foodmanager.objects.filter(user=user)

    #@csrf_exempt
    def Update(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = FoodSerializer(queryset, many=True)
        return Response(serializer.data)

class FoodDestroy(generics.DestroyAPIView):
    queryset = Foodmanager.objects.all()
    serializer_class = FoodSerializer

    def get_queryset(self):
        user = self.request.user
        return Foodmanager.objects.filter(user=user)

    #@csrf_exempt
    def Destroy(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = FoodSerializer(queryset, many=True)
        return Response(serializer.data)
