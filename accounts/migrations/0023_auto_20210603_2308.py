# Generated by Django 3.1.7 on 2021-06-03 16:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20210603_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seanses',
            name='time_of_begin',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 3, 16, 8, 5, 925094, tzinfo=utc)),
        ),
    ]
