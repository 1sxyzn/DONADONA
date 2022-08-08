# Generated by Django 3.1.3 on 2022-08-07 19:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import donadona.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('nickname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=128, null=True)),
                ('phone', models.CharField(max_length=11, unique=True)),
                ('alarm', models.BooleanField(default=False)),
                ('hours', models.IntegerField(default=0)),
                ('point', models.IntegerField(default=0)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', donadona.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('able_category', models.CharField(choices=[('생활', '생활')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(choices=[('서울특별시', '서울특별시'), ('경기도', '경기도'), ('강원도', '강원도'), ('충청북도', '충청북도'), ('충청남도', '충청남도'), ('전라북도 ', '전라북도'), ('전라남도 ', '전라남도'), ('경상북도', '경상북도'), ('경상남도', '경상남도'), ('부산광역시', '부산광역시'), ('인천광역시', '인천광역시'), ('대구광역시', '대구광역시'), ('대전광역시 ', '대전광역시'), ('광주광역시 ', '광주광역시'), ('울산광역시', '울산광역시'), ('세종특별자치시', '세종특별자치시'), ('제주특별자치도', '제주특별자치도')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_week', models.CharField(choices=[('Monday', '월요일'), ('Tuesday', '화요일'), ('Wednesday', '수요일'), ('Thursday', '목요일'), ('Friday', '금요일'), ('Saturday ', '토요일'), ('Sunday ', '일요일')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)])),
                ('end_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)])),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donadona.day')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=1000)),
                ('hour', models.IntegerField()),
                ('solved_flag', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('help_day_week', models.CharField(choices=[('Monday', '월요일'), ('Tuesday', '화요일'), ('Wednesday', '수요일'), ('Thursday', '목요일'), ('Friday', '금요일'), ('Saturday ', '토요일'), ('Sunday ', '일요일')], max_length=20)),
                ('help_star_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)])),
                ('help_city', models.CharField(choices=[('서울특별시', '서울특별시'), ('경기도', '경기도'), ('강원도', '강원도'), ('충청북도', '충청북도'), ('충청남도', '충청남도'), ('전라북도 ', '전라북도'), ('전라남도 ', '전라남도'), ('경상북도', '경상북도'), ('경상남도', '경상남도'), ('부산광역시', '부산광역시'), ('인천광역시', '인천광역시'), ('대구광역시', '대구광역시'), ('대전광역시 ', '대전광역시'), ('광주광역시 ', '광주광역시'), ('울산광역시', '울산광역시'), ('세종특별자치시', '세종특별자치시'), ('제주특별자치도', '제주특별자치도')], max_length=20)),
                ('help_si_gun_gu', models.CharField(max_length=20)),
                ('help_addr_detail', models.CharField(blank=True, max_length=100, null=True)),
                ('help_able_category', models.CharField(choices=[('생활', '생활')], max_length=20)),
                ('help_able_detail', models.CharField(blank=True, max_length=100, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('helper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='helper', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AddressDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('si_gun_gu', models.CharField(max_length=20)),
                ('addr_detail', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donadona.address')),
            ],
        ),
        migrations.CreateModel(
            name='AbilityDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('able_detail', models.CharField(blank=True, max_length=100, null=True)),
                ('ability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donadona.ability')),
            ],
        ),
    ]
