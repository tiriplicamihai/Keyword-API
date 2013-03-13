import factory
import random
from models import *

class OwnerFactory(factory.Factory):
    @classmethod
    def _prepare(cls, create, **kwargs):
        stream_number = kwargs.pop('stream_number', None)
        owner = super(OwnerFactory, cls)._prepare(create, **kwargs)

        if stream_number:
            owner.set_stream_number(stream_number)
        if create:
            owner.save()
        return owner


    username = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))


class StreamFactory(factory.Factory):
    @classmethod
    def _prepare(cls, create, **kwargs):
        owner = kwargs.pop('owner', None)
        name = kwargs.pop('name', None)
        language = kwargs.pop('language', None)
        location = kwargs.pop('location', None)
        stream = super(StreamFactory, cls)._prepare(create, **kwargs)

        if owner:
            stream.set_owner(owner)
        if name:
            stream.set_name(name)
        if language:
            stream.set_language(language)
        if location:
            stream.set_location(location)
        if create:
            stream.save()
        return stream


    owner = factory.SubFactory(OwnerFactory)
    name = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))


class KeywordFactory(factory.Factory):
    FACTORY_FOR = Keyword

    stream = factory.SubFactory(StreamFactory)
    word = factory.Sequence(lambda n: 'TestKeyWord {0}'.format(n))

