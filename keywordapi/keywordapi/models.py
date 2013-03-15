from tastypie.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from model_constants import KeywordConstants

class Owner(User):
    """
     Contains information about accounts (companies) owners.
    """
    stream_number = models.IntegerField(default=15)


class Stream(models.Model):
    """
     Contains informations about one owner streams.
    """

    owner = models.ForeignKey(Owner, related_name='streams', unique=False)
    name = models.CharField(max_length=200)
    date = models.DateField(default=now)
    language = models.CharField(max_length=200, default='English')
    location = models.CharField(max_length=200, default='US')


class Keyword(models.Model):
    """
     Contains the keywords selected by a owner for a stream.
    """
    stream = models.ForeignKey(Stream, related_name='keywords', unique=False)
    word = models.CharField(max_length=60)
    key_type = models.CharField(max_length=1, choices=KeywordConstants.TYPES, default='A')

