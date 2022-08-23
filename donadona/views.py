from django.shortcuts import render, redirect
from .models import *
from .forms import *


def main(request):
    return render(request, 'donadona/main.html')


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

            Day.objects.filter(user=user, day_week=day_week).delete()
            user_day = Day.objects.create(user=user, day_week=day_week)
            user_time = Time.objects.get_or_create(day=user_day, start_time=start_time, end_time=end_time)
            return redirect('donadona:info')
    else:
        form = UserDayForm()
    context = {'form': form}
    return render(request, 'donadona/user_day_form.html', context)


def userAddress(request):
    form = UserAddressForm()
    return render(request, 'donadona/user_address_form.html', {'form': form})


def userAbility(request):
    form = UserAbilityForm()
    return render(request, 'donadona/user_ability_form.html', {'form': form})
