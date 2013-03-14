import copy
from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from tastypie import fields
from keywordapi.models import *

class MetaBase:
    excludes = ['id']
    include_resource_uri = False

class KeywordResource(ModelResource):

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])
            return data_dict

    class Meta(MetaBase):
        queryset = Keyword.objects.all()
        resource_name = 'keywords'
        authentication = BasicAuthentication()
        authorization = Authorization()

class StreamResource(ModelResource):
    keyword = fields.ToManyField('keywordapi.api.KeywordResource',
                            'keywords')

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])
            return data_dict

    class Meta(MetaBase):
        queryset = Stream.objects.all()
        resource_name = 'streams'
        authentication = BasicAuthentication()
        authorization = Authorization()

class OwnerResource(ModelResource):
    stream = fields.ToManyField('keywordapi.api.StreamResource',
                            'streams')

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])
            return data_dict

    class Meta(MetaBase):
        queryset = Owner.objects.all()
        resource_name = 'owners'
        always_return_data = True
        fields = ['username', 'stream_number']
        authorization = Authorization()
        authentication = BasicAuthentication()
