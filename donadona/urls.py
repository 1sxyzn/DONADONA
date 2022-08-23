from django.urls import path
from . import views

app_name = 'donadona'

urlpatterns = [
    path('', views.main, name='main'),
    path('manual', views.manual, name='manual'),
    path('mypage', views.mypage, name='mypage'),
    path('user-info', views.userInfo, name='user-info'),
]
