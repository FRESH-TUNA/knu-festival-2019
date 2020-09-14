import importlib
import re
import os
import inspect
import logging
from functools import reduce
from django.conf import settings
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from rest_framework.viewsets import ModelViewSet

from rest_framework.renderers import (
    TemplateHTMLRenderer,
    JSONRenderer
)

class BaseGenericViewSet(ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    # queryset
    # lookup_field = 'comment_pk'
    
    # Note: Views are made CSRF exempt from within `as_view` as to prevent
    # accidental removal of this exemption in cases where `dispatch` needs to
    # be overridden.
    def dispatch(self, request, *args, **kwargs):
        setattr(self, 'model', self.get_model(self.get_resource()))
        method = request.POST.get('_method', None)
        request.method = method if method is not None else request.method

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.all()
        reference_object = None
        reference_object_reference_name = None
        
        for parent_resource in self.get_parent_resources():
            parent_queryset = self.get_model(parent_resource).objects.all()

            if reference_object is not None:
                parent_queryset = parent_queryset.filter({
                    reference_object_reference_name: reference_object
                })
                        
            reference_object_reference_name = ''.join(list(parent_resource)[:-1])
            pk = self.kwargs["%s_pk" % reference_object_reference_name]
            reference_object = get_object_or_404(queryset, pk=pk)

        if reference_object is None:
            return queryset
        else:
            return queryset.filter({
                reference_object_reference_name: reference_object
            })

    def get_serializer_class(self):
        index_action = ['list', 'create']
        show_action = ['retrieve', 'update', 'delete']

        if self.serializer_class is not None:
            return super().get_serializer_class()

        parent_resources = self.get_parent_resources()
        resource = self.get_resource()

        serializer_path = "%s.serializers%s" % (
            self.request.resolver_match.app_name,
            reduce(
                lambda path, cur: "." + path + cur.lower(), parent_resources, ""
            )
        )

        if self.action in index_action :
            serializer_name = "%s_%s" % (resource, "list_serializer")  
        else:
            serializer_name = "%s_%s" % (resource, "detail_serializer")

        serializer_path += ".%s" % serializer_name

        serializer_name = self.camelize_snake(serializer_name)
        return getattr(
            __import__(serializer_path, globals(), locals(), [serializer_name], 0),
            serializer_name
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_template_name_suffix(self):
        index_action = ['list', 'delete', 'create']
        show_action = ['retrieve', 'update']

        if self.action in index_action:
            return ".list"
        elif self.action in show_action:
            return ".detail"
        else:
            return ".%s" % self.action

    def get_parent_resources_template_prefix(self):
        return reduce(
            lambda model, cur: cur + "%s/" % model.lower(), 
            self.get_parent_resources(), ""
        )

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        # if self.template_name is None:
        #     return super().get_template_names()
        
        names = []

        if hasattr(self, 'model'):
            opts = self.model._meta
            names.append("%s/%s%ss%s.html" % (
                    opts.app_label, 
                    self.get_parent_resources_template_prefix(),
                    opts.model_name, 
                    self.get_template_name_suffix()
                )
            )
        else: # model이 없으면 에러 발생
            raise ImproperlyConfigured(
                "%(cls)s requires either a 'template_name' attribute "
                "or a get_queryset() method that returns a QuerySet." % {
                    'cls': self.__class__.__name__,
                }
            )
        return names


    def get_resource(self):
        return inspect.getfile(self.__class__).split('/')[-1].split('_')[0]

    def get_parent_resources(self):
        parent_resources = list(reversed(inspect.getfile(self.__class__).split('/')))[:-4]
        if len(parent_resources) == 1:
            return []
        else:
            return parent_resources[1:]            

    def get_model(self, parent_resource):
        model_path = "%s.models" % self.request.resolver_match.app_name
        model_name = list(parent_resource)
        model_name[0] = model_name[0].upper()
        model_name = ''.join(model_name[:-1])
        return getattr(
            __import__(model_path, globals(), locals(), [model_name], 0),
            model_name
        )  

    def camelize_snake(self, sentence):
        return ''.join(x.title() for x in sentence.split('_'))
