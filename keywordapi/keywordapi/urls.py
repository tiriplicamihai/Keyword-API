from django.conf.urls.defaults import *

from keywordapi.api import *

owner_resource = OwnerResource()
stream_resource = StreamResource()
keyword_resource = KeywordResource()

urlpatterns = patterns('',
    url(r'^api/', include(owner_resource.urls)),
    url(r'^api/', include(stream_resource.urls)),
    url(r'^api/', include(keyword_resource.urls)),
)
