from django.db import models
from django.contrib.auth.models import User

class Owner(User):
    stream_number = models.IntegerField(default=15)

    def get_stream_number(self):
        return self.stream_number

