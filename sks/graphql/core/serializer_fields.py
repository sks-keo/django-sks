'''
Created on Jun 20, 2018

@author: keakseysum
'''
import itertools
from rest_framework import serializers
from slugify import slugify
from rest_framework.fields import empty

class Field(object):
    
    def __init__(self, *args, **kwargs):
        self._cach_required = kwargs.get('required')
        kwargs['required']  = False
        super(Field, self).__init__(*args, **kwargs)
    
    def run_cach_required(self):
        if self._cach_required:
            self.required = True
        
    def run_validation(self, data=empty):
        
        self.run_cach_required()
        
        return super(Field, self).run_validation(data)
    
class DecimalField(Field, serializers.DecimalField):
    pass

class CharField(Field, serializers.CharField):
    pass

class IntegerField(Field, serializers.IntegerField):
    pass

class AutoHandleField(serializers.SlugField):
    
    def __init__(self, **kwargs):
        self.model_auto_handle = kwargs.pop('model_auto_handle', None)
        self.field_name = kwargs.pop('field_name', 'handle')
        self.uniqe_by   = kwargs.pop('uniqe_by')
        
        super(AutoHandleField, self).__init__(**kwargs)
        
    def to_internal_value(self, handle):
        
        if not handle:
            return handle
        
        handle = slugify(handle)
        
        request = self.context['request']
        
        queryset = self.model_auto_handle.objects.all()
        
        instance = getattr(self.root, 'instance')
        
        if instance:
            queryset = queryset.exclude(id=instance.id)
        
        if self.uniqe_by == 'shop':
            queryset = queryset.filter(shop=request.shop)
        elif self.uniqe_by == 'site':
            queryset = queryset.filter(site=request.shop.site)
            
        for x in itertools.count(1):
            query_field = {
                self.field_name+'__iexact': handle
            }
            
            if not queryset.filter(**query_field).exists():
                break
            
            try:
                handle_strs = handle.split('-')
                x = int(handle_strs[-1]) + x
                
                handle = '-'.join(handle_strs[0:len(handle_strs)-1])
            except Exception:
                pass
            
            handle = "%s-%s" % (handle, x)
            
        return handle
