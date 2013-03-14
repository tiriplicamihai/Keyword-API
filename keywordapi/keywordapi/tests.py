import unittest
import json
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.utils.timezone import now
from nose.tools import ok_, eq_, istest
from keywordapi.models import Owner, Stream, Keyword
from keywordapi.factories import *


class OwnerTest(TestCase):
    def test_default_stream_number(self):
        owner = OwnerFactory()
        eq_(owner.stream_number, 15)

    def test_stream_number(self):
        owner = OwnerFactory(stream_number=20)
        ok_(owner.stream_number!=15)
        eq_(owner.stream_number, 20)


class StreamTest(TestCase):
    def setUp(self):
        self.owner = OwnerFactory()

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
        self.owner = OwnerFactory()
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


class OwnerResourceTest(ResourceTestCase):
    def setUp(self):
        super(OwnerResourceTest, self).setUp()

        self.username = 'user_test'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'test@test.com',
                self.password)
        self.owner_1 = OwnerFactory()
        self.detail_url = '/api/owner/list/{0}/'.format(self.owner_1.pk)
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
        self.assertHttpUnauthorized(self.api_client.get('/api/owner/list/', format='json'))

    def test_get_list_json(self):
        resp = self.api_client.get('/api/owner/list/', format='json',
                authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    def test_post_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.post('/api/owner/list/',
            format='json', data=self.post_data))

    def test_post_list(self):
        owner_no = Owner.objects.count()
        self.assertHttpCreated(self.api_client.post('/api/owner/list/',
            format='json', data=self.post_data,
            authentication=self.get_credentials()))
        self.assertEqual(Owner.objects.count(), owner_no + 1)

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
        self.assertEqual(Owner.objects.count(), owner_no)
        self.assertEqual(Owner.objects.get(pk=self.owner_1.pk).stream_number, 60)

    def test_delete_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url,
            format='json'))

    def test_delete(self):
        owner_no = Owner.objects.count()
        self.assertHttpAccepted(self.api_client.delete(self.detail_url,
            format='json', authentication=self.get_credentials()))
        self.assertEqual(Owner.objects.count(), owner_no - 1)


class StreamResourceTest(ResourceTestCase):
    def setUp(self):
        super(StreamResourceTest, self).setUp()

        self.username = 'user_test'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'test@test.com',
                self.password)
        self.owner = OwnerFactory()
        self.stream = StreamFactory()
        self.detail_url = '/api/stream/list/{0}/'.format(self.stream.pk)
        self.post_data = {
                'name': 'newteststream',
                'owner': self.owner.pk,
                'keyword': [],
                'language': 'Romanian',
                'location': 'RO'
                }

    def get_credentials(self):
        return self.create_basic(username=self.username,
                password=self.password)

    def test_get_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/stream/list/', format='json'))

    def test_get_list(self):
        resp = self.api_client.get('/api/stream/list/', format='json',
                authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    def test_post_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.post('/api/stream/list/',
            format='json', data=self.post_data))

    def test_post_list(self):
        stream_no = Stream.objects.count()
        self.assertHttpCreated(self.api_client.post('/api/stream/list/',
            format='json', data=self.post_data,
            authentication=self.get_credentials()))
        self.assertEqual(Stream.objects.count(), stream_no + 1)

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

        self.assertEqual(Stream.objects.count(), stream_no)
        self.assertEqual(Stream.objects.get(pk=self.stream.pk).language, 'French')
        self.assertEqual(Stream.objects.get(pk=self.stream.pk).name, 'test')
        self.assertEqual(Stream.objects.get(pk=self.stream.pk).location, 'UK')

    def test_delete_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url,
            format='json'))

    def test_delete(self):
        stream_no = Stream.objects.count()
        self.assertHttpAccepted(self.api_client.delete(self.detail_url,
            format='json', authentication=self.get_credentials()))
        self.assertEqual(Stream.objects.count(), stream_no - 1)


class KeywordResourceTest(ResourceTestCase):
    def setUp(self):
        super(KeywordResourceTest, self).setUp()

        self.username = 'user_test'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'test@test.com',
                self.password)
        self.owner = OwnerFactory()
        self.stream = StreamFactory()
        self.keyword = KeywordFactory()
        self.detail_url = '/api/keyword/list/{0}/'.format(self.keyword.pk)
        self.post_data = {
                'word': 'newkey',
                'stream': self.stream.pk,
                'key_type': 'O'
                }

    def get_credentials(self):
        return self.create_basic(username=self.username,
                password=self.password)

    def test_get_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/keyword/list/',
            format='json'))

    def test_get_list(self):
        resp = self.api_client.get('/api/keyword/list/', format='json',
                authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    def test_post_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.post('/api/keyword/list/',
            format='json', data=self.post_data))

    def test_post_list(self):
        keyword_no = Keyword.objects.count()
        self.assertHttpCreated(self.api_client.post('/api/keyword/list/',
            format='json', data=self.post_data,
            authentication=self.get_credentials()))
        self.assertEqual(Keyword.objects.count(), keyword_no + 1)

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

        self.assertEqual(Keyword.objects.count(), keyword_no)
        kw = Keyword.objects.get(pk=self.keyword.pk)
        self.assertEqual(kw.word, 'keyword')
        self.assertEqual(kw.key_type, 'N')

    def test_delete_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url,
            format='json'))

    def test_delete(self):
        keyword_no = Keyword.objects.count()
        self.assertHttpAccepted(self.api_client.delete(self.detail_url,
            format='json', authentication=self.get_credentials()))
        self.assertEqual(Keyword.objects.count(), keyword_no - 1)

