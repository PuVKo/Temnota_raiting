# Generated by Django 3.2.18 on 2023-03-20 12:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20230315_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='regdate',
            field=models.DateField(default=datetime.datetime(2023, 3, 20, 22, 41, 26, 2859), verbose_name='Дата внесения'),
        ),
        migrations.AlterField(
            model_name='game',
            name='gamedate',
            field=models.DateField(default=datetime.datetime(2023, 3, 20, 22, 41, 26, 2836), verbose_name='Дата игры'),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Никнейм'),
        ),
        migrations.AlterField(
            model_name='raiting',
            name='registerdate',
            field=models.DateField(default=datetime.datetime(2023, 3, 20, 22, 41, 25, 958980), verbose_name='Дата игры'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 3, 20, 22, 41, 26, 4251), verbose_name='Дата проведения турнира'),
        ),
    ]