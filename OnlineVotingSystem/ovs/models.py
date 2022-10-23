from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import string
import random

alphaN = 3
numN = 7

letters = string.ascii_letters
nums = string.digits

# Create your models here.
class UserProfile(models.Model):
    randomVid = "".join((random.choice(letters[26:]) for i in range(alphaN))) + "".join((random.choice(nums) for i in range(numN)))
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    vid = models.CharField(max_length=11, default=randomVid)
    address = models.CharField(max_length=100, default="")
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=100, default="")
    phone = models.IntegerField(default=0)
    head_shot = models.ImageField(upload_to='profile_images', blank=True)
    voted = models.BooleanField(default=False)
    #imgName = models.CharField(max_length=100, default="")
    class Meta:
        ordering = ["user"]

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.get_or_create(user=kwargs['instance'])



class Party(models.Model):
    party_name = models.CharField(max_length=50, default='', null=False)
    party_symbol = models.ImageField(upload_to='party_symbols', default='', null=False)
    vote_count = models.IntegerField(default=0)

    def getParty(self, id):
        model = Party
        partyobj = model.objects.get(id=id)
        return partyobj

# def voteCount():
#     print(Party.objects.get(id=1).party_name)

# voteCount()

# class Vote(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     party_name = models.CharField(max_length=50, default="")
#
#
#     class Meta:
#         ordering = ["user"]
#
#     def __str__(self):
#         return self.user.username
#
#
#
# def create_voting(sender, **kwargs):
#     if kwargs['created']:
#         user_voting = Vote.objects.get_or_create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
# post_save.connect(create_voting, sender=User)
