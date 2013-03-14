import factory
import random
from models import *

class OwnerFactory(factory.Factory):
    username = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))
    stream_number = random.randint(0, 60)


class StreamFactory(factory.Factory):
    owner = factory.SubFactory(OwnerFactory)
    name = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))
    language = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))
    location = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))

class KeywordFactory(factory.Factory):
    stream = factory.SubFactory(StreamFactory)
    word = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))
    key_type = random.choice(['A', 'N', 'O'])

