import unittest
from django.contrib.auth.models import User
from django.test import TestCase
from django.db import IntegrityError
from nose.tools import ok_, eq_, raises
from keywordapi.models import Owner, Stream, Keyword
from keywordapi.factories import *


class OwnerTest(TestCase):
    @raises(IntegrityError)
    def test_unique_key(self):
        owner = OwnerFactory.build()
        owner.username = None
        owner.save()

class StreamTest(TestCase):
    @raises(ValueError)
    def test_null_value(self):
        stream = StreamFactory.build()
        stream.owner = None
        stream.save()


class KeyWordTest(TestCase):
    @raises(ValueError)
    def test_null_value(self):
        keyword = KeywordFactory.build()
        keyword.stream = None
        keyword.save()
