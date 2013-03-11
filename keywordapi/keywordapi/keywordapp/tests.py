import unittest
import json
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCase
from keywordapi.keywordapp.models import Owner, Stream, Keyword


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


class KeywordTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(username='test')
        self.stream = Stream.objects.create(owner=self.owner)

    def test_set_stream(self):
        key = Keyword.objects.create(stream=self.stream)
        self.assertTrue(key.get_stream().id==self.stream.id)

    def test_default_key_type(self):
        key = Keyword.objects.create(stream=self.stream)
        self.assertEqual(key.get_key_type(), 'A')

    def test_set_key_type(self):
        ktype = 'O';
        key = Keyword.objects.create(stream=self.stream, key_type=ktype)
        self.assertEqual(key.get_key_type(), ktype)

        ktype = 'N'
        key.set_key_type(ktype)
        self.assertEqual(key.get_key_type(), ktype)

        ktype = 'T'
        key.set_key_type(ktype)
        self.assertFalse(key.get_key_type()==ktype)

    def test_set_word(self):
        word = 'test'
        key = Keyword.objects.create(stream=self.stream, word=word)
        self.assertEqual(key.get_word(), word)

        word = 'newtest'
        key.set_word(word)
        self.assertEqual(key.get_word(), word)


class OwnerResourceTest(ResourceTestCase):
    def setUp(self):
        super(OwnerResourceTest, self).setUp()

        self.username = 'user_test'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'test@test.com',
                self.password)
        self.owner_1 = Owner.objects.create(username="testowner",
                stream_number=30)
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


