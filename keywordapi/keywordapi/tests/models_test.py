import unittest
from django.contrib.auth.models import User
from django.test import TestCase
from nose.tools import ok_, eq_, istest
from keywordapi.models import Owner, Stream, Keyword
from keywordapi.factories import *


class OwnerTest(TestCase):
    def test_default_stream_number(self):
        owner = OwnerFactory.build()
        eq_(owner.stream_number, 15)

    def test_stream_number(self):
        owner = OwnerFactory(stream_number=20)
        ok_(owner.stream_number!=15)
        eq_(owner.stream_number, 20)


class StreamTest(TestCase):
    def setUp(self):
        self.owner = OwnerFactory.build()

    def test_set_owner(self):
        stream = StreamFactory(owner=self.owner)
        eq_(stream.owner.id, self.owner.id)

    def test_set_name(self):
        name = 'test1'
        stream = StreamFactory(owner=self.owner, name=name)
        eq_(stream.name, name)

    def test_default_location(self):
        stream = StreamFactory(owner=self.owner)
        eq_(stream.location, 'US')

    def test_set_location(self):
        location = 'RO'
        stream = StreamFactory(owner=self.owner, location=location)
        eq_(stream.location, location)


    def test_default_language(self):
        stream = StreamFactory(owner=self.owner)
        eq_(stream.language, 'English')

    def test_set_language(self):
        language = 'Romanian'
        stream = StreamFactory(owner=self.owner, language=language)
        eq_(stream.language, language)


class KeywordTest(TestCase):
    def setUp(self):
        self.owner = OwnerFactory.build()
        self.stream = StreamFactory(owner=self.owner)

    def test_set_stream(self):
        key = KeywordFactory(stream=self.stream)
        eq_(key.stream.id, self.stream.id)

    def test_default_key_type(self):
        key = KeywordFactory(stream=self.stream)
        eq_(key.key_type, 'A')

    def test_set_key_type(self):
        ktype = 'O';
        key = KeywordFactory(stream=self.stream, key_type=ktype)
        eq_(key.key_type, ktype)

    def test_set_word(self):
        word = 'test'
        key = KeywordFactory(stream=self.stream, word=word)
        eq_(key.word, word)


