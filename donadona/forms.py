from django import forms
from donadona.models import *


DAY_CHOICE = [
        ('월요일', '월요일'),
        ('화요일', '화요일'),
        ('수요일', '수요일'),
        ('목요일', '목요일'),
        ('금요일', '금요일'),
        ('토요일 ', '토요일'),
        ('일요일 ', '일요일'),
    ]

CITY_CHOICE = [
    ('서울특별시', '서울특별시'),
    ('경기도', '경기도'),
    ('강원도', '강원도'),
    ('충청북도', '충청북도'),
    ('충청남도', '충청남도'),
    ('전라북도 ', '전라북도'),
    ('전라남도 ', '전라남도'),
    ('경상북도', '경상북도'),
    ('경상남도', '경상남도'),
    ('부산광역시', '부산광역시'),
    ('인천광역시', '인천광역시'),
    ('대구광역시', '대구광역시'),
    ('대전광역시 ', '대전광역시'),
    ('광주광역시 ', '광주광역시'),
    ('울산광역시', '울산광역시'),
    ('세종특별자치시', '세종특별자치시'),
    ('제주특별자치도', '제주특별자치도'),
]


ABLE_CHOICE = [
    ('생활', '생활'),
    ('환경', '환경'),
    ('식사', '식사'),
    ('동행', '동행'),
    ('안전', '안전'),
    ('운동', '운동'),
    ('의료', '의료'),
    ('상담', '상담'),
    ('문화', '문화'),
    ('교육', '교육'),
    ('정서', '정서'),
    ('취미', '취미'),
    ('외국어', '외국어'),
    ('IT', 'IT'),
]


class UserDayForm(forms.Form):
    day_week = forms.ChoiceField(choices=DAY_CHOICE)
    start_time = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])
    end_time = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])

    fields = ['day_week', 'start_time', 'end_time']


class UserAddressForm(forms.Form):
    city = forms.ChoiceField(choices=CITY_CHOICE)
    si_gun_gu = forms.CharField(max_length=20)
    addr_detail = forms.CharField(max_length=100)

    fields = ['city', 'si_gun_gu', 'addr_detail']


class UserAbilityForm(forms.Form):
    able_category = forms.ChoiceField(choices=ABLE_CHOICE)
    able_detail = forms.CharField(max_length=100)

    fields = ['able_category', 'able_detail']


class HelpResolutionForm(forms.Form):
    helper = forms.CharField(max_length=20)
    time = forms.IntegerField()

    fields = ['helper', 'time']


class HelpRequestForm(forms.Form):
    title = forms.CharField(max_length=20)
    content = forms.CharField(max_length=1000)

    hour = forms.IntegerField()
    date = forms.DateField()
    time = forms.TimeField()

    city = forms.ChoiceField(choices=CITY_CHOICE)
    si_gun_gu = forms.CharField(max_length=20)
    addr_detail = forms.CharField(max_length=100)

    able_category = forms.ChoiceField(choices=ABLE_CHOICE)
    able_detail = forms.CharField(max_length=100)

    fields = ['title', 'content',
              'hour', 'date', 'time',
              'city', 'si_gun_gu', 'addr_detail',
              'able_category', 'able_detail']
