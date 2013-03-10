"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import unittest
import json

from django.test import TestCase
from keywordapi.keywordapp.models import Owner


class OwnerTest(TestCase):
    def test_default_stream_number(self):
        owner = Owner.objects.create(username='test')
        self.assertTrue(owner.get_stream_number()==15)

    def test_stream_number(self):
        owner = Owner.objects.create(username='test', stream_number=20)
        self.assertFalse(owner.get_stream_number()==15)
        self.assertTrue(owner.get_stream_number()==20)
