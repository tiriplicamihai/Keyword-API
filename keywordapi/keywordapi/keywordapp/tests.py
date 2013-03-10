import unittest
import json

from django.test import TestCase
from keywordapi.keywordapp.models import Owner, Stream


class OwnerTest(TestCase):
    def test_default_stream_number(self):
        owner = Owner.objects.create(username='test')
        self.assertTrue(owner.get_stream_number()==15)

    def test_stream_number(self):
        owner = Owner.objects.create(username='test', stream_number=20)
        self.assertFalse(owner.get_stream_number()==15)
        self.assertTrue(owner.get_stream_number()==20)


class StreamTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(username='test')

    def test_set_owner(self):
        stream = Stream.objects.create(owner=self.owner)
        self.assertTrue(stream.get_owner().id==self.owner.id)

        new_owner = Owner.objects.create(username='test2')
        stream.set_owner(new_owner)
        self.assertTrue(stream.get_owner().id==new_owner.id)

    def test_set_name(self):
        name = 'test1'
        stream = Stream.objects.create(owner=self.owner, name=name)
        self.assertTrue(stream.get_name()==name)

        new_name = 'test2'
        stream.set_name(new_name)
        self.assertTrue(stream.get_name()==new_name)

    def test_default_location(self):
        stream = Stream.objects.create(owner=self.owner)
        self.assertTrue(stream.get_location()=='US')

    def test_set_location(self):
        location = 'RO'
        stream = Stream.objects.create(owner=self.owner, location=location)
        self.assertTrue(stream.get_location()==location)

        new_location = 'UK'
        stream.set_location(new_location)
        self.assertTrue(stream.get_location()==new_location)

    def test_default_language(self):
        stream = Stream.objects.create(owner=self.owner)
        self.assertTrue(stream.get_language()=='English')

    def test_set_language(self):
        language = 'Romanian'
        stream = Stream.objects.create(owner=self.owner, language=language)
        self.assertTrue(stream.get_language()==language)

        new_language = 'Hindu'
        stream.set_language(new_language)
        self.assertTrue(stream.get_language()==new_language)

