# Generated by Django 3.1.3 on 2022-09-01 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donadona', '0003_auto_20220823_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='helper',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='helper', to=settings.AUTH_USER_MODEL),
        ),
    ]
