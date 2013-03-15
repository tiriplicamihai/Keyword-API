from tastypie.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from model_constants import KeywordConstants

class Owner(User):
    """
     Contains information about accounts (companies) owners.
    """
    stream_number = models.IntegerField(default=15,
                        help_text='Number of streams available for a user')


class Stream(models.Model):
    """
     Contains informations about one owner streams.
    """

    owner = models.ForeignKey(Owner, related_name='streams', unique=False,
                            help_text='Owner of the stream')
    name = models.CharField(max_length=200,
                            help_text='May contain any available character')
    date = models.DateField(default=now,
                            help_text='It will be set automatically when the stream is created')
    language = models.CharField(max_length=200, default='English')
    location = models.CharField(max_length=200, default='US')


class Keyword(models.Model):
    """
     Contains the keywords selected by a owner for a stream.
    """
    stream = models.ForeignKey(Stream, related_name='keywords', unique=False,
            help_text='Filtered stream')
    word = models.CharField(max_length=60,
                help_text='The keyword may contain any available character')
    key_type = models.CharField(max_length=1, choices=KeywordConstants.TYPES, default='A')

