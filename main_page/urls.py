"""Home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
import main_page
from main_page import views
urlpatterns = [
    url(r'^$',main_page.views.display,name='main_page'),
    url(r'^managemember/$',main_page.views.manage_member,name='managemember'),
    url(r'^delete/$',main_page.views.delete,name='delete'),
    url(r'^expendituredetail/$',main_page.views.expendituredetail,name='expendituredetail'),
    url(r'^updateexp/$',main_page.views.update_exp,name='update_exp'),
    url(r'^exp_getdetail/$', main_page.views.exp_getdetail, name='exp_getdetail'),
    url(r'^exp_getdetailbydate/$', main_page.views.exp_getdetailbydate, name='getdetailbydate'),
    url(r'^expenditurereport/$', main_page.views.expenditurereport, name='expreport'),
    url(r'^expenditurereportbydate/$', main_page.views.expenditurereportbydate, name='expreportbydate'),
    url(r'^deletedetail/$', main_page.views.deletedetail, name='deletedetail'),

]
