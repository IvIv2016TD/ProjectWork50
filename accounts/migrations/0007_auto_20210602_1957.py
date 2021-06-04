# Generated by Django 3.1.7 on 2021-06-02 12:57

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0006_auto_20210525_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='data_of_registration',
            field=models.DateField(default=datetime.date(2021, 6, 2)),
        ),
        migrations.CreateModel(
            name='Seanses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_begin', models.DateField(auto_now=True)),
                ('time_of_end', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
