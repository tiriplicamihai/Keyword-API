import factory
import random
from models import *
from model_constants import KeywordConstants

class OwnerFactory(factory.Factory):
    """
     Generates random Owner objects.
    """
    username = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))
    stream_number = random.randint(0, 60)


class StreamFactory(factory.Factory):
    """
     Generates random Stream objects.
    """
    owner = factory.SubFactory(OwnerFactory)
    name = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))
    language = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))
    location = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))

class KeywordFactory(factory.Factory):
    """
     Generates random Keyword objects.
    """
    stream = factory.SubFactory(StreamFactory)
    word = factory.LazyAttribute(lambda n: '%030x' % random.randrange(256 ** 15))
    key_type = random.choice(KeywordConstants.list_comprehension())

