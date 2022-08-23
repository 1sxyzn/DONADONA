from django import forms
from donadona.models import *


DAY_CHOICE = [
        ('Monday', '월요일'),
        ('Tuesday', '화요일'),
        ('Wednesday', '수요일'),
        ('Thursday', '목요일'),
        ('Friday', '금요일'),
        ('Saturday ', '토요일'),
        ('Sunday ', '일요일'),
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

# Coming Soon..
ABLE_CHOICE = [
    ('생활', '생활')
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
