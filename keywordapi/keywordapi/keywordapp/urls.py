from django.conf.urls.defaults import *

from keywordapi.keywordapp.api import *

owner_resource = OwnerResource()

urlpatterns = patterns('',
    url(r'^api/', include(owner_resource.urls)),
)
