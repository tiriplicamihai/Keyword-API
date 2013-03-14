import unittest
import json
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.utils.timezone import now
from nose.tools import ok_, eq_, istest
from keywordapi.models import Owner, Stream, Keyword
from keywordapi.factories import *


class OwnerResourceTest(ResourceTestCase):
    def setUp(self):
        super(OwnerResourceTest, self).setUp()

        self.username = 'user_test'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'test@test.com',
                self.password)
        self.owner_1 = OwnerFactory()
        self.detail_url = '/api/v1/owners/{0}/'.format(self.owner_1.pk)
        self.post_data = {
                'username': 'newowner',
                'password': 'pass',
                'stream': [],
                'stream_number': 25
                }

    def get_credentials(self):
        return self.create_basic(username=self.username,
                password=self.password)

    def test_get_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/v1/owners/', format='json'))

    def test_get_list_json(self):
        resp = self.api_client.get('/api/v1/owners/', format='json',
                authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    def test_post_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.post('/api/v1/owners/',
            format='json', data=self.post_data))

    def test_post_list(self):
        owner_no = Owner.objects.count()
        self.assertHttpCreated(self.api_client.post('/api/v1/owners/',
            format='json', data=self.post_data,
            authentication=self.get_credentials()))
        eq_(Owner.objects.count(), owner_no + 1)

    def test_put_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.put(self.detail_url,
            format='json', data={}))

    def test_put(self):
        original_data = self.deserialize(self.api_client.get(self.detail_url,
            format='json', authentication=self.get_credentials()))

        new_data = original_data.copy()
        new_data['stream_number'] = 60
        owner_no = Owner.objects.count()
        self.assertHttpAccepted(self.api_client.put(self.detail_url,
            format='json', data=new_data,
            authentication=self.get_credentials()))
        eq_(Owner.objects.count(), owner_no)
        eq_(Owner.objects.get(pk=self.owner_1.pk).stream_number, 60)

    def test_delete_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url,
            format='json'))

    def test_delete(self):
        owner_no = Owner.objects.count()
        self.assertHttpAccepted(self.api_client.delete(self.detail_url,
            format='json', authentication=self.get_credentials()))
        eq_(Owner.objects.count(), owner_no - 1)

