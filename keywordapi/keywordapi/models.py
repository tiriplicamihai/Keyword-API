from tastypie.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User

class Owner(User):
    stream_number = models.IntegerField(default=15)


class Stream(models.Model):
    owner = models.ForeignKey(Owner, related_name='streams', null=True)
    name = models.CharField(max_length=200)
    date = models.DateField(default=now)
    language = models.CharField(max_length=200, default='English')
    location = models.CharField(max_length=200, default='US')


class Keyword(models.Model):
    TYPE = (
        ('A', 'Must contain'),
        ('O', 'May contain'),
        ('N', 'Must not contain'),
    )

    stream = models.ForeignKey(Stream, related_name='keywords', null=True)
    word = models.CharField(max_length=60)
    key_type = models.CharField(max_length=1, choices=TYPE, default='A')
