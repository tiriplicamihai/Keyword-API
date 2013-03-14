import unittest
import json
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.utils.timezone import now
from nose.tools import ok_, eq_, istest
from keywordapi.models import Owner, Stream, Keyword
from keywordapi.factories import *


class KeywordResourceTest(ResourceTestCase):
    fixtures = ['test_entries.json']
    def setUp(self):
        super(KeywordResourceTest, self).setUp()

        self.username = 'user_test'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'test@test.com',
                self.password)
        self.owner = OwnerFactory()
        self.stream = StreamFactory()
        self.keyword = KeywordFactory()
        self.detail_url = '/api/v1/keywords/{0}/'.format(self.keyword.pk)
        self.post_data = {
                'word': 'newkey',
                'stream': '/api/v1/streams/{0}/'.format(self.stream.pk),
                'key_type': 'O'
                }

    def get_credentials(self):
        return self.create_basic(username=self.username,
                password=self.password)

    def test_get_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/v1/keywords/',
            format='json'))

    def test_get_list(self):
        resp = self.api_client.get('/api/v1/keywords/', format='json',
                authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    def test_post_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.post('/api/v1/keywords/',
            format='json', data=self.post_data))

    def test_post_list(self):
        keyword_no = Keyword.objects.count()
        self.assertHttpCreated(self.api_client.post('/api/v1/keywords/',
            format='json', data=self.post_data,
            authentication=self.get_credentials()))
        eq_(Keyword.objects.count(), keyword_no + 1)

    def test_put_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.put(self.detail_url,
            format='json', data={}))

    def test_put(self):
        keyword_no = Keyword.objects.count()
        original_data = self.deserialize(self.api_client.get(self.detail_url,
            format='json', authentication=self.get_credentials()))

        new_data = original_data.copy()
        new_data['word'] = 'keyword'
        new_data['key_type'] = 'N'

        self.assertHttpAccepted(self.api_client.put(self.detail_url,
            format='json', data=new_data,
            authentication=self.get_credentials()))

        eq_(Keyword.objects.count(), keyword_no)
        kw = Keyword.objects.get(pk=self.keyword.pk)
        eq_(kw.word, 'keyword')
        eq_(kw.key_type, 'N')

    def test_delete_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url,
            format='json'))

    def test_delete(self):
        keyword_no = Keyword.objects.count()
        self.assertHttpAccepted(self.api_client.delete(self.detail_url,
            format='json', authentication=self.get_credentials()))
        eq_(Keyword.objects.count(), keyword_no - 1)

