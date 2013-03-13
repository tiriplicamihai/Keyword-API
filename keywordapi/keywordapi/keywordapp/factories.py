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
    stream_number = 15


class StreamFactory(factory.Factory):
    FACTORY_FOR = Stream

    owner = factory.SubFactory(OwnerFactory)
    name = factory.Sequence(lambda n: 'TestStream {0}'.format(n))


class KeywordFactory(factory.Factory):
    FACTORY_FOR = Keyword

    stream = factory.SubFactory(StreamFactory)
    word = factory.Sequence(lambda n: 'TestKeyWord {0}'.format(n))

