import json

from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import datetime, date
import hashlib
import hmac
import base64
import requests
import time
from decouple import config

timestamp = int(time.time() * 1000)
timestamp = str(timestamp)
access_key = config('SENS_ACCESS_KEY')
url = "https://sens.apigw.ntruss.com"
uri = "/sms/v2/services/" + config('SENS_SERVICE_ID') + "/messages"


def make_signature():
    secret_key = config('SENS_SECRET_KEY')
    secret_key = bytes(secret_key, 'UTF-8')

    method = "POST"

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey


def day_week_calc(date):
    days = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    day = date.weekday()
    return (days[day])


def main(request):
    return render(request, 'donadona/main.html')


def helpList(request):
    help_list = Post.objects.all()
    context = {'help_list': help_list}
    return render(request, 'donadona/help_list.html', context)


def helpRequest(request):
    if request.method == 'POST':
        form = HelpRequestForm(request.POST)
        if form.is_valid():
            title = request.POST['title']
            content = request.POST['content']
            hour = request.POST['hour']

            help_date = request.POST['date']
            dates = help_date.split('-')
            year = int(dates[0])
            month = int(dates[1])
            day = int(dates[2])
            help_day_week = day_week_calc(date(year, month, day))

            help_time = request.POST['time']
            help_city = request.POST['city']
            help_si_gun_gu = request.POST['si_gun_gu']
            help_addr_detail = request.POST['addr_detail']
            help_able_category = request.POST['able_category']
            help_able_detail = request.POST['able_detail']

            Post.objects.create(
                author=request.user, title=title, content=content,
                hour=hour, help_day_week=help_day_week, help_date=help_date, help_time=help_time,
                help_city=help_city, help_si_gun_gu=help_si_gun_gu, help_addr_detail=help_addr_detail,
                help_able_category=help_able_category, help_able_detail=help_able_detail
            )
            return redirect('donadona:list')
    else:
        form = HelpRequestForm()
    context = {'form': form}
    return render(request, 'donadona/help_request_form.html', context)


def help(request, help_id):  # 도움 주기

    phone_num = Post.objects.get(pk=help_id).author.phone

    header = {
        "Content-Type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": config('SENS_ACCESS_KEY'),
        "x-ncp-apigw-signature-v2": make_signature(),
    }

    data = {
        "type": "SMS",
        "from": config('SENS_PHONE_NUM'),
        "content": "[도나도나]",  # max 80byte, 기본 메시지 제목
        "messages": [
            {
                "to": phone_num,  # 수신 번호
                "content": "[도나도나] ID : " + str(request.user) + "\n"
                           + str(request.user.nickname) + "님께서 도움을 주시기로 하셨어요!\n"
                           + str(request.user.phone) + "으로 연락해보세요!"  # 개별 메시지 내용
            }
        ]
    }
    res = requests.post(url + uri, headers=header, data=json.dumps(data))
    print(res.text)
    return redirect('donadona:list')  # Send SMS


def resolution(request, help_id):
    if request.method == 'POST':
        form = HelpResolutionForm(request.POST)
        if form.is_valid():
            helper = request.POST['helper']
            time = request.POST['time']

            try:
                user = User.objects.get(username=helper)
            except:
                return render(request, 'error.html')

            user.hours = user.hours + int(time)
            user.point = user.point + int(time) * 500
            user.save()

            post = Post.objects.get(pk=help_id)
            post.solved_flag = True
            post.helper = user
            post.save()
            return redirect('donadona:list')
    else:
        form = HelpResolutionForm()
    context = {'form': form}
    return render(request, 'donadona/helper_form.html', context)


def manual(request):
    return render(request, 'donadona/manual.html')


def mypage(request):
    return render(request, 'donadona/mypage.html')


def userInfo(request):
    return render(request, 'donadona/user_info.html')


def userDay(request):
    if request.method == 'POST':
        form = UserDayForm(request.POST)
        if form.is_valid():
            day_week = request.POST['day_week']
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            user = request.user

            user_day = Day.objects.get_or_create(user=user, day_week=day_week)
            Time.objects.create(day=user_day[0], start_time=start_time, end_time=end_time)
            return redirect('donadona:info')
    else:
        form = UserDayForm()
    context = {'form': form}
    return render(request, 'donadona/user_day_form.html', context)


def userAddress(request):
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            city = request.POST['city']
            si_gun_gu = request.POST['si_gun_gu']
            addr_detail = request.POST['addr_detail']
            user = request.user

            user_addr = Address.objects.get_or_create(user=user, city=city)
            AddressDetail.objects.create(address=user_addr[0], si_gun_gu=si_gun_gu, addr_detail=addr_detail)
            return redirect('donadona:info')
    else:
        form = UserAddressForm()
    context = {'form': form}
    return render(request, 'donadona/user_address_form.html', context)


def userAbility(request):
    if request.method == 'POST':
        form = UserAbilityForm(request.POST)
        if form.is_valid():
            able_category = request.POST['able_category']
            able_detail = request.POST['able_detail']
            user = request.user

            user_able = Ability.objects.get_or_create(user=user, able_category=able_category)
            AbilityDetail.objects.create(ability=user_able[0], able_detail=able_detail)
            return redirect('donadona:info')
    else:
        form = UserAbilityForm()
    context = {'form': form}
    return render(request, 'donadona/user_ability_form.html', context)
