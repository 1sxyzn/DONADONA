from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.validators import MinValueValidator, MaxValueValidator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, nickname, phone, password, email=None):
        if not username:
            raise ValueError('아이디는 필수 항목 입니다.')
        if not nickname:
            raise ValueError('이름은 필수 항목 입니다.')
        if not phone:
            raise ValueError('전화번호는 필수 항목 입니다.')
        if not password:
            raise ValueError('비밀번호는 필수 항목 입니다.')

        user = self.model(
            username=username,
            nickname=nickname,
            email=self.normalize_email(email),
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, nickname, email=None, phone=None, password=None):
        user = self.create_user(
            username=username,
            nickname=nickname,
            email=self.normalize_email(email),
            phone=phone,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    username = models.CharField(max_length=15, unique=True)
    nickname = models.CharField(max_length=5)
    email = models.EmailField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True)
    alarm = models.BooleanField(default=False)
    hours = models.IntegerField(default=0)
    point = models.IntegerField(default=0)

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone', 'nickname']

    def __str__(self):
        return self.username


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


class Day(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_week = models.CharField(max_length=20, choices=DAY_CHOICE)

    def __str__(self):
        return '{}. {} : {}'.format(self.pk, self.user, self.day_week)


class Time(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    start_time = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])
    end_time = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=20, choices=CITY_CHOICE)

    def __str__(self):
        return '{}. {} : {}'.format(self.pk, self.user, self.city)


class AddressDetail(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    si_gun_gu = models.CharField(max_length=20)
    addr_detail = models.CharField(max_length=100, null=True, blank=True)


class Ability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    able_category = models.CharField(max_length=20, choices=ABLE_CHOICE)

    def __str__(self):
        return '{}. {} : {}'.format(self.pk, self.user, self.able_category)


class AbilityDetail(models.Model):
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    able_detail = models.CharField(max_length=100, null=True, blank=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    helper = models.ForeignKey(User, on_delete=models.CASCADE, related_name='helper', null=True, blank=True)
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=1000)
    hour = models.IntegerField()  # 소요 시간
    solved_flag = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    help_day_week = models.CharField(max_length=20, choices=DAY_CHOICE)
    help_date = models.CharField(max_length=20, default='YYYY-MM-DD')  # 날짜
    help_time = models.CharField(max_length=20, default='HH:MM')  # 시작 시간
    help_city = models.CharField(max_length=20, choices=CITY_CHOICE)
    help_si_gun_gu = models.CharField(max_length=20)
    help_addr_detail = models.CharField(max_length=100, null=True, blank=True)
    help_able_category = models.CharField(max_length=20, choices=ABLE_CHOICE)
    help_able_detail = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '{}. {} : {}'.format(self.pk, self.author, self.title)

