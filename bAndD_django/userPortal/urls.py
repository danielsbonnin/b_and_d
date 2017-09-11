from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from userPortal.views import ChildDetailView, UpdateBlocksView
from userPortal.views import UpdateDollarsView, UpdateMinutesView
from userPortal.views import DailyReportDetailView, BuyMinutesView
from userPortal.views import ScreentimePrereqsView, Index
from userPortal.views import logout as userPortalLogout
from userPortal.views import login as userPortalLogin, IXLReportView
from userPortal.views import CoinStoreView, CoinItemRequestView
from userPortal.forms import ScreentimePrereqsForm

app_name = 'userPortal'
urlpatterns = [
    url(r'^$', Index.as_view(), name='users home'),
    url(r'login-child/', userPortalLogin, name='child login'),
    url(r'login/', login, kwargs={'template_name': 'userPortal/login.html', 'extra_context': {'next': '/userPortal/login-child/'}}, 
        name='user login'),
    url(r'^logout-child/', userPortalLogout, name='child logout'),
    url(r'^logout/', logout, kwargs={'next_page': '/userPortal/login'}, name='logout'),
    url(r'^child/(?P<pk>[0-9]+)/$', ChildDetailView.as_view(), name='child-detail'),
    url(r'^daily-requirements-report/(?P<pk>[0-9]+)/$', 
        DailyReportDetailView.as_view(), name='daily-report-detail'),
    url(r'^child/(?P<pk>[0-9]+)/blocks/$', UpdateBlocksView.as_view(),
        name='update-blocks'),
    url(r'^child/(?P<pk>[0-9]+)/dollars/$', UpdateDollarsView.as_view(),
        name='update-dollars'),
    url(r'^child/(?P<pk>[0-9]+)/minutes-left/$', UpdateMinutesView.as_view(),
        name='update-minutes-left'),
    url(r'^child/(?P<pk>[0-9]+)/daily-requirements/$', 
        ScreentimePrereqsView.as_view(), name='daily-requirements'),
    url(r'^child/(?P<pk>[0-9]+)/buy-minutes/$', 
        BuyMinutesView.as_view(), name='buy-minutes'),
    url(r'^child/(?P<pk>[0-9]+)/ixl-report/$',
        IXLReportView.as_view(), name='ixl-report'),
    url(r'^child/(?P<pk>[0-9]+)/coin-store/$',
        CoinStoreView.as_view(), name='coin store'),
    url(r'^child/(?P<pk>[0-9]+)/store-item-request/$',
        CoinItemRequestView.as_view(), name='store item request'),
]
