# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from rest_framework.authtoken.models import Token
# Create your models here.

class Question(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=datetime.now, blank=False)
    # country =  models.CharField(null=True,blank=True,max_length=60)
    # city = models.CharField(null=True,blank=True,max_length=60,db_index=True)
    # zipcode = models.CharField(null=True,blank=True,max_length=10)

    def __str__(self):
        return self.question

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)