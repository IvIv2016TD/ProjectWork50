# Generated by Django 3.1.7 on 2021-06-03 15:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20210603_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seanses',
            name='number_of_points_read',
            field=models.IntegerField(default=555),
        ),
        migrations.AlterField(
            model_name='seanses',
            name='number_of_points_write',
            field=models.IntegerField(default=777),
        ),
        migrations.AlterField(
            model_name='seanses',
            name='time_of_begin',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 3, 15, 4, 14, 351974, tzinfo=utc)),
        ),
    ]
