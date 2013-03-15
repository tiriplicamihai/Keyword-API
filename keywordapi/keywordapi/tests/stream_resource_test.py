import unittest
import json
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.utils.timezone import now
from nose.tools import ok_, eq_, istest
from keywordapi.models import Owner, Stream, Keyword
from keywordapi.factories import *


class StreamResourceTest(ResourceTestCase):
    def setUp(self):
        super(StreamResourceTest, self).setUp()

        self.username = 'user_test'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'test@test.com',
                self.password)
        self.owner = OwnerFactory()
        self.stream = StreamFactory()
        self.detail_url = '/api/v1/streams/{0}/'.format(self.stream.pk)
        self.post_data = {
                'name': 'newteststream',
                'owner': '/api/v1/owners/{0}/'.format(self.owner.pk),
                'keyword': [],
                'language': 'Romanian',
                'location': 'RO'
                }

    def get_credentials(self):
        return self.create_basic(username=self.username,
                password=self.password)

    def test_get_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/v1/streams/', format='json'))

    def test_get_list(self):
        resp = self.api_client.get('/api/v1/streams/', format='json',
                authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    def test_post_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.post('/api/v1/streams/',
            format='json', data=self.post_data))

    def test_post_list(self):
        stream_no = Stream.objects.count()
        self.assertHttpCreated(self.api_client.post('/api/v1/streams/',
            format='json', data=self.post_data,
            authentication=self.get_credentials()))
        eq_(Stream.objects.count(), stream_no + 1)

    def test_put_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.put(self.detail_url,
            format='json', data={}))

    def test_put(self):
        stream_no = Stream.objects.count()
        original_data = self.deserialize(self.api_client.get(self.detail_url, format='json',
                authentication=self.get_credentials()))

        new_data = original_data.copy()
        new_data['language'] = 'French'
        new_data['name'] = 'test'
        new_data['location'] = 'UK'

        self.assertHttpAccepted(self.api_client.put(self.detail_url,
            format='json', data=new_data,
            authentication=self.get_credentials()))

        eq_(Stream.objects.count(), stream_no)
        eq_(Stream.objects.get(pk=self.stream.pk).language, 'French')
        eq_(Stream.objects.get(pk=self.stream.pk).name, 'test')
        eq_(Stream.objects.get(pk=self.stream.pk).location, 'UK')

    def test_delete_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url,
            format='json'))

    def test_delete(self):
        stream_no = Stream.objects.count()
        self.assertHttpAccepted(self.api_client.delete(self.detail_url,
            format='json', authentication=self.get_credentials()))
        eq_(Stream.objects.count(), stream_no - 1)

