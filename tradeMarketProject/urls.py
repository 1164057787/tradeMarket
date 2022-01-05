"""tradeMarketProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from app01 import views,urls



urlpatterns = [
        # path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('test/',views.test),

    re_path('admins/(?P<pk>\d+)', views.AdminView.as_view()),
    #d第一种写法的路由 ，单个操作

    path('admins/', views.AdminsView.as_view()),

    path('users/', views.UsersView.as_view()),

    path('cates/', views.CategoryView.as_view()) ,  #查所有种类的路由

    #include 路由分发
    path('app01/',include(urls))



]
