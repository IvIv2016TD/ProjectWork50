# Generated by Django 3.1.7 on 2021-06-20 07:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_auto_20210620_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupshr',
            name='time_of_registration',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 20, 7, 45, 3, 877640, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='seanses',
            name='time_of_begin',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 20, 7, 45, 3, 875642, tzinfo=utc)),
        ),
    ]
