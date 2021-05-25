from django.db import models
import datetime

# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):

    SINGLE_USER = 'SU'
    GROUP_MEMBER = 'GM'
    TEAM_LEADER = 'TL'
    STATUS_OF_USER_CHOICES = [
        (SINGLE_USER, 'Одиночный пользователь'),
        (GROUP_MEMBER, 'Член группы'),
        (TEAM_LEADER, 'Руководитель группы'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    status_of_user = models.CharField(max_length=50, choices=STATUS_OF_USER_CHOICES, default=SINGLE_USER, blank=True)
    data_of_registration = models.DateField(default=datetime.date.today())
    time_of_last_visit = models.DateTimeField(auto_now=True)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
		
    def is_upperclass(self):
        return self.status_of_user in {self.GROUP_MEMBER, self.TEAM_LEADER}

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()