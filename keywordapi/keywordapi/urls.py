from django.conf.urls.defaults import *
from tastypie.api import Api
from keywordapi.api import *

v1_api = Api(api_name='v1')
v1_api.register(OwnerResource())
v1_api.register(StreamResource())
v1_api.register(KeywordResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
)
