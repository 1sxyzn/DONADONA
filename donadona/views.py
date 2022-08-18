from django.shortcuts import render
from .models import *


def main(request):
    return render(request, 'donadona/main.html')


def manual(request):
    return render(request, 'donadona/manual.html')


def mypage(request):
    return render(request, 'donadona/mypage.html')


def survey(request):
    return render(request, 'donadona/survey.html')

