from tastypie.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User

class Owner(User):
    stream_number = models.IntegerField(default=15)

    def get_stream_number(self):
        return self.stream_number

class Stream(models.Model):
    owner = models.ForeignKey(Owner, related_name='streams', null=True)
    name = models.CharField(max_length=200)
    date = models.DateField(default=now)
    language = models.CharField(max_length=200, default='English')
    location = models.CharField(max_length=200, default='US')

    def get_owner(self):
        return self.owner

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location

    def get_language(self):
        return self.language

    def set_owner(self, owner):
        self.owner = owner
        self.save()

    def set_name(self, name):
        self.name = name
        self.save()

    def set_location(self, location):
        self.location = location
        self.save()

    def set_language(self, language):
        self.language = language
        self.save()


class Keyword(models.Model):
    TYPE = (
        ('A', 'Must contain'),
        ('O', 'May contain'),
        ('N', 'Must not contain'),
    )

    stream = models.ForeignKey(Stream, related_name='keywords', null=True)
    word = models.CharField(max_length=60)
    key_type = models.CharField(max_length=1, choices=TYPE, default='A')

    def set_stream(self, stream):
        self.stream = stream;
        self.save()

    def set_key_type(self, ktype):
        for t in self.TYPE:
            if ktype in t:
                self.key_type = ktype
                self.save()

    def set_word(self, word):
        self.word = word
        self.save()

    def get_stream(self):
        return self.stream

    def get_key_type(self):
        return self.key_type

    def get_word(self):
        return self.word

