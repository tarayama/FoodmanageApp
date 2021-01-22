from rest_framework import serializers
from django.contrib.auth.models import User, Group
from foodmanager.models import FoodCategory, Foodmanager
from django.contrib.auth import get_user_model 


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ('id', 'user', 'name')

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foodmanager
        fields = ('id', 'user', 'name', 'memo', 'category', 'limit', 'solution')
