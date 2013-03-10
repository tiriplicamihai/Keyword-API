import copy
from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from keywordapi.keywordapp.models import *

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

class KeywordResource(ModelResource):
    class Meta:
        queryset = Keyword.objects.all()
        resource_name = 'keyword/list'
        include_resource_uri = False
        authorization = Authorization()

class StreamResource(ModelResource):
    keyword = fields.ToManyField('keywordapi.keywordapp.api.KeywordResource',
                            'keywords')

    class Meta:
        queryset = Stream.objects.all()
        resource_name = 'stream/list'
        include_resource_uri = False
        authorization = Authorization()

class OwnerResource(ModelResource):
    stream = fields.ToManyField('keywordapi.keywordapp.api.StreamResource',
                            'streams')

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
        include_resource_uri = False
        always_return_data = True
        authorization = Authorization()
        allowed_methods = ['get', 'post']
