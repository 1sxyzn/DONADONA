from django.urls import path
from . import views

app_name = 'donadona'

urlpatterns = [
    path('', views.main, name='main'),
    path('help/list', views.helpList, name='list'),  # 도움 목록
    path('help/request', views.helpRequest, name='request'),  # 도움 요청
    path('help/<int:help_id>', views.help, name='help'),  # 도움 주기
    path('resolution/<int:help_id>', views.resolution, name='resolution'),  # 도움 해결

    path('manual', views.manual, name='manual'),
    path('ranking', views.ranking, name='ranking'),

    path('mypage', views.mypage, name='mypage'),
    path('mypage/help/list', views.mypageHelp, name='myhelp'),
    path('mypage/info', views.mypageInfo, name='myinfo'),

    path('info', views.userInfo, name='info'),
    path('info/day', views.userDay, name='day'),
    path('info/address', views.userAddress, name='address'),
    path('info/ability', views.userAbility, name='ability'),
]
