import factory
import random
from models import *

class OwnerFactory(factory.Factory):
    # Generates random Owner objects. Will be changed in
    # f/#24-validation-tests-branch

    @classmethod
    def _prepare(cls, create, **kwargs):
        stream_number = kwargs.pop('stream_number', None)
        owner = super(OwnerFactory, cls)._prepare(create, **kwargs)

        if stream_number:
            owner.stream_number = stream_number
        if create:
            owner.save()
        return owner


    username = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))


class StreamFactory(factory.Factory):
    # Generates random Stream objects. Will be changed in
    # f/#24-validation-tests-branch

    @classmethod
    def _prepare(cls, create, **kwargs):
        owner = kwargs.pop('owner', None)
        name = kwargs.pop('name', None)
        language = kwargs.pop('language', None)
        location = kwargs.pop('location', None)
        stream = super(StreamFactory, cls)._prepare(create, **kwargs)

        if owner:
            stream.owner = owner
        if name:
            stream.name = name
        if language:
            stream.language = language
        if location:
            stream.location = location
        if create:
            stream.save()
        return stream


    owner = factory.SubFactory(OwnerFactory)
    name = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))


class KeywordFactory(factory.Factory):
    # Generates random Keyword objects. Will be changed in
    # f/#24-validation-tests-branch

    @classmethod
    def _prepare(cls, create, **kwargs):
        stream = kwargs.pop('stream', None)
        word = kwargs.pop('word', None)
        key_type = kwargs.pop('key_type', None)
        keyword = super(KeywordFactory, cls)._prepare(create, **kwargs)

        if stream:
            keyword.stream = stream
        if word:
            keyword.word = word
        if key_type:
            keyword.key_type = key_type
        if create:
            keyword.save()
        return keyword


    stream = factory.SubFactory(StreamFactory)
    word = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))

