import factory
import random
from models import *

class OwnerFactory(factory.Factory):
    FACTORY_FOR = Owner

    stream_number = random.randint(0, 100)
    username = factory.Sequence(lambda n: 'TestOwner {0}'.format(n))


class StreamFactory(factory.Factory):
    FACTORY_FOR = Stream

    owner = factory.SubFactory(OwnerFactory)
    name = factory.Sequence(lambda n: 'TestStream {0}'.format(n))


class KeywordFactory(factory.Factory):
    FACTORY_FOR = Keyword

    stream = factory.SubFactory(StreamFactory)
    word = factory.Sequence(lambda n: 'TestKeyWord {0}'.format(n))

