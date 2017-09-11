"""bAndD_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout
from adminPortal import views as adminPortalViews
from adminPortal import models as adminPortalModels

app_name = 'adminPortal'
urlpatterns = [
    url(r'^$', adminPortalViews.Index.as_view(), name='admin home'),
    url(r'login/', login, kwargs={
        'template_name': 'adminPortal/login.html', 
        'extra_context': {'next':'/adminPortal/'}
        }, name='admin login'),
    url(r'^logout/', logout, kwargs={'next_page': '/adminPortal/login'},
        name='admin logout'),
    url(r'^parent/(?P<pid>[0-9]+)/children/', 
        adminPortalViews.ChildrenListView.as_view(), name='children list'),
    url(r'^parent/(?P<pid>[0-9]+)/child/(?P<cid>[0-9]+)/daily-report/(?P<pk>[0-9]+)/',
        adminPortalViews.DailyRequirementsReportDetail.as_view(),
        name='daily-report'),
    url(
        r'^parent/(?P<pid>[0-9]+)/coin-store-review/',
        adminPortalViews.CoinStoreReview.as_view(),
        name='coin store review'),
    #url(),
]