# Generated by Django 3.1.7 on 2021-06-03 15:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20210603_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seanses',
            name='time_of_begin',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 3, 15, 19, 56, 644700, tzinfo=utc)),
        ),
    ]
