# Generated by Django 3.2.18 on 2023-03-15 04:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20230315_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gamedate',
            field=models.DateField(default=datetime.datetime(2023, 3, 15, 14, 12, 39, 720142), verbose_name='Дата игры'),
        ),
        migrations.AlterField(
            model_name='raiting',
            name='registerdate',
            field=models.DateField(default=datetime.datetime(2023, 3, 15, 14, 12, 39, 670318), verbose_name='Дата игры'),
        ),
    ]