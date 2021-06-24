from django.db import models
import datetime
from django.utils import timezone

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

class Seanses(models.Model):

    user = models.CharField(max_length=100, blank=True)
    time_of_begin = models.DateTimeField(default=timezone.now())
    time_of_end = models.DateTimeField(auto_now=True)
    number_of_points_write = models.IntegerField(default=0)
    number_of_points_read = models.IntegerField(default=0)

    def __str__(self):
        return "Seanses of Users"
    
    @classmethod
    def create_seanse(cls, name_user, output_time_of_begin, number_of_points_write, number_of_points_read):
        seanse = cls(user = name_user, time_of_begin = output_time_of_begin, 
                    number_of_points_write = number_of_points_write, 
                    number_of_points_read = number_of_points_read)
        return seanse

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
	
class Groupshr(models.Model):

    user = models.CharField(max_length=100, blank=True)
    name_of_grouphr = models.CharField(max_length=100, blank=True)
    time_of_registration = models.DateTimeField(default=timezone.now())
    comment_of_TL = models.CharField(max_length=1000, blank=True)
    operating_grouphr = models.BooleanField(default=False)

    def __str__(self):
        return "Groups of Users"
    
    @classmethod
    def create_grouphr(cls, name_user, name_of_grouphr, time_of_registration, comment_of_TL):
        grouphr = cls(user = name_user, name_of_group = name_of_grouphr, 
                    time_of_registration = time_of_registration, 
                    comment_of_TL = comment_of_TL,
					operating_grouphr = True)
        return grouphr