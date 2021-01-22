from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='index'),
    path('top',views.top, name='top'),
    path('new_food',views.new_Food, name='new'),
    
    path('jancode/<int:jancode>',views.jancode_to_productname, name='jancode'),
    path('postal_code/<int:postal_code>', views.post_to_foodbank, name='foodbank'),
    path('GetLimit', csrf_exempt(views.Image_to_Limit), name='limit') #これはまだ開発中
]
