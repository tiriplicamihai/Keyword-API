from tastypie.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User

class Owner(User):
    stream_number = models.IntegerField(default=15)

    def get_stream_number(self):
        return self.stream_number

class Stream(models.Model):
    owner = models.ForeignKey(Owner)
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

    def set_name(self, name):
        self.name = name

    def set_location(self, location):
        self.location = location

    def set_language(self, language):
        self.language = language

