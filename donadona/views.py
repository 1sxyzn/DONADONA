from django.shortcuts import render, redirect
from .models import *
from .forms import *


def main(request):
    return render(request, 'donadona/main.html')


def helpList(request):
    help_list = Post.objects.all()
    context = {'help_list': help_list}
    return render(request, 'donadona/help_list.html', context)


def help(request, help_id):
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
            user_time = Time.objects.create(day=user_day[0], start_time=start_time, end_time=end_time)
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
            user_addr_detail = AddressDetail.objects.create(address=user_addr[0], si_gun_gu=si_gun_gu, addr_detail=addr_detail)
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
            user_able_detail = AbilityDetail.objects.create(ability=user_able[0], able_detail=able_detail)
            return redirect('donadona:info')
    else:
        form = UserAbilityForm()
    context = {'form': form}
    return render(request, 'donadona/user_ability_form.html', context)
