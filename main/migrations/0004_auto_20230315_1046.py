# Generated by Django 3.2.10 on 2023-03-15 00:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20230228_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Никнейм')),
            ],
        ),
        migrations.AddField(
            model_name='raiting',
            name='ball',
            field=models.FloatField(default=0, verbose_name='Баллы'),
        ),
        migrations.AddField(
            model_name='raiting',
            name='itog',
            field=models.FloatField(default=0, verbose_name='Средний балл'),
        ),
        migrations.AddField(
            model_name='raiting',
            name='losses',
            field=models.IntegerField(default=0, verbose_name='Лузы'),
        ),
        migrations.AddField(
            model_name='raiting',
            name='med_ball',
            field=models.FloatField(default=0, verbose_name='Средний балл'),
        ),
        migrations.AddField(
            model_name='raiting',
            name='nowinner',
            field=models.IntegerField(default=0, verbose_name='Ничья'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='raiting',
            name='threered',
            field=models.IntegerField(default=0, verbose_name='3 красных'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='raiting',
            name='total_game',
            field=models.IntegerField(default=0, verbose_name='Всего игр'),
        ),
        migrations.AddField(
            model_name='raiting',
            name='total_loose',
            field=models.IntegerField(default=0, verbose_name='Всего поражений'),
        ),
        migrations.AddField(
            model_name='raiting',
            name='total_win',
            field=models.IntegerField(default=0, verbose_name='Всего побед'),
        ),
        migrations.AddField(
            model_name='raiting',
            name='winrate',
            field=models.IntegerField(default=0, verbose_name='% побед'),
        ),
        migrations.AlterField(
            model_name='game',
            name='gamedate',
            field=models.DateField(default=datetime.datetime(2023, 3, 15, 10, 45, 44, 567131), verbose_name='Дата игры'),
        ),
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.CharField(choices=[('maf', 'Мафия'), ('mir', 'Мирные'), ('not', 'Ничья')], default='mir', max_length=3, verbose_name='Победившая команда'),
        ),
        migrations.AlterField(
            model_name='raiting',
            name='compens',
            field=models.IntegerField(verbose_name='Компенсация'),
        ),
        migrations.AlterField(
            model_name='raiting',
            name='registerdate',
            field=models.DateField(default=datetime.datetime(2023, 3, 15, 10, 45, 44, 510325), verbose_name='Дата игры'),
        ),
    ]
