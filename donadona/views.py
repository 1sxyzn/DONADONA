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
    return days[day]


def main(request):
    return render(request, 'donadona/main.html')


def ranking(request):
    users = User.objects.order_by('-hours')
    context = {'users': users}
    return render(request, 'donadona/ranking.html', context)


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
            hour_minute = help_time.split(':')
            help_start_time = int(hour_minute[0])

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

            users = User.objects.filter(alarm=True)
            helper_phone = []
            for user in users:
                if request.user != user:
                    try:
                        addr = Address.objects.get(user=user, city=help_city)
                        AddressDetail.objects.filter(address=addr, si_gun_gu=help_si_gun_gu)
                        Ability.objects.get(user=user, able_category=help_able_category)
                        day = Day.objects.get(user=user, day_week=help_day_week)
                        times = Time.objects.filter(day=day)
                        for t in times:
                            if t.start_time <= help_start_time and t.end_time >= (help_start_time + int(hour)):
                                helper_phone.append(user.phone)
                    except:
                        pass

            for phone_num in helper_phone:
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
                            "content": str(request.user.nickname) + "님께서 도움을 요청했어요!\n"  # 개별 메시지 내용
                                       + "[요청] " + title + "\n"
                                       + "[날짜] " + help_date
                        }
                    ]
                }
                res = requests.post(url + uri, headers=header, data=json.dumps(data))
            return redirect('donadona:list')
    else:
        form = HelpRequestForm()
    context = {'form': form}
    return render(request, 'donadona/help_request_form.html', context)


def help(request, help_id):  # 도움 주기

    post = Post.objects.get(pk=help_id)
    phone_num = post.author.phone

    header = {
        "Content-Type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": config('SENS_ACCESS_KEY'),
        "x-ncp-apigw-signature-v2": make_signature(),
    }

    data = {
        "type": "LMS",
        "from": config('SENS_PHONE_NUM'),
        "content": "[도나도나]",  # max 80byte, 기본 메시지 제목
        "messages": [
            {
                "to": phone_num,  # 수신 번호
                "content": str(request.user.nickname) + "님께서 도와주신대요!\n"
                            + "[번호] " + str(request.user.phone) + "\n"
                            + "[아이디] " + str(request.user)

                            + "\n\n" + str(post.help_able_detail) + "에 관련된 [ " + str(post.title) + " ] 를 도와주실 수 있으시대요.\n"
                            + "연락을 통해 도움을 받아보세요 :)\n\n"
                            + "※ 도움을 받으신 후, 해결되었다면 게시글 하단의 \"도움 해결\" 버튼을 눌러주세요.\n"
                            + "※ \"도움 해결\" 버튼을 누르지 않으시거나 허위사실을 기재하시면 서비스를 이용하시는 데에 불이익이 발생할 수 있습니다."
                # SMS 용
                # "content": str(request.user.nickname) + "님께서 도와주신대요\n"
                #            + str(request.user.phone) + "로 연락해보세요!\n"
                #            + "ID: " + str(request.user)
            }
        ]
    }
    res = requests.post(url + uri, headers=header, data=json.dumps(data))
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
