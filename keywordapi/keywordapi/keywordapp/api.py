import copy
from tastypie.resources import ModelResource
from tastypie import fields
from keywordapi.keywordapp.models import *

class KeywordResource(ModelResource):
    class Meta:
        queryset = Keyword.objects.all()
        excludes = ['id']
        include_resource_uri = False

class StreamResource(ModelResource):
    keywords = fields.OneToManyField('keywordapi.keywordapp.api.KeywordResource',
                            'keywords', full=True)

    class Meta:
        queryset = Stream.objects.all()
        excludes = ['id']
        include_resource_uri = False

class OwnerResource(ModelResource):
    streams = fields.OneToManyField('keywordapi.keywordapp.api.StreamResource',
                            'streams', full=True)

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])
                data_dict['Owners'] = copy.copy(data_dict['objects'])
                del(data_dict['objects'])
            return data_dict

    class Meta:
        queryset = Owner.objects.all()
        resource_name = 'owner/list'
        fields = ['username', 'stream_number']
        include_resource_uri = False

