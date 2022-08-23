from django.urls import path
from . import views

app_name = 'donadona'

urlpatterns = [
    path('', views.main, name='main'),
    path('manual', views.manual, name='manual'),
    path('mypage', views.mypage, name='mypage'),

    path('info/', views.userInfo, name='info'),
    path('info/day', views.userDay, name='day'),
    path('info/address', views.userAddress, name='address'),
    path('info/ability', views.userAbility, name='ability'),
]
