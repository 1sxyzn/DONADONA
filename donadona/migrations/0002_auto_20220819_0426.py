# Generated by Django 3.1.3 on 2022-08-18 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donadona', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=128, null=True),
        ),
    ]