from django.urls import path,re_path,include
from app01 import views

urlpatterns = [

    re_path('goods/(?P<pk>\d+)', views.GoodsView.as_view()) ,  #查所有种类的路由

]