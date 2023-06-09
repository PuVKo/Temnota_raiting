# Generated by Django 4.1.7 on 2023-05-21 07:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20230504_1356'),
    ]

    operations = [
        migrations.CreateModel(
            name='FullSeason',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('season', models.CharField(max_length=20, verbose_name='Название сезона')),
                ('year', models.IntegerField(default=0, verbose_name='Год')),
                ('date1', models.DateField(default='Null', verbose_name='Начало первого месяца в числовом формате')),
                ('date2', models.DateField(default='Null', verbose_name='Начало второго месяца в числовом формате')),
                ('date3', models.DateField(default='Null', verbose_name='Начало третьего месяца в числовом формате')),
            ],
        ),
        migrations.RemoveField(
            model_name='raiting',
            name='registerdate',
        ),
        migrations.AlterField(
            model_name='game',
            name='gamedate',
            field=models.DateField(default=datetime.datetime(2023, 5, 21, 17, 5, 8, 61092), verbose_name='Дата игры'),
        ),
        migrations.AlterField(
            model_name='game',
            name='regdate',
            field=models.DateField(default=datetime.datetime(2023, 5, 21, 17, 5, 8, 61092), verbose_name='Дата внесения'),
        ),
    ]
