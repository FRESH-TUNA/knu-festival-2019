import importlib
import re
import os
import inspect
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

class BaseView(ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    # lookup_field = 'comment_pk'
    ## dispatch ##
    def dispatch(self, request, *args, **kwargs):
        # delete, update, patch... support
        def restful_support(request):
            method = request.POST.get('_method', None)
            return method if method is not None else request.method

        request.method = restful_support(request)
        return super().dispatch(request, *args, **kwargs)

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        super().initial(request, *args, **kwargs)

        # autoloading resource related module
        self.autoload_model()
        self.autoload_queryset()
        self.autoload_serializer()
        self.autoload_paginator()
        self.autoload_template()

    ## autoloading ##
    def autoload_model(self):
        if getattr(self, 'model', None) is None:
            setattr(self, 'model', self.get_model(self.get_resource()))
    
    def autoload_serializer(self):
        if getattr(self, 'serializer_class', None) is None:
            index_action = ['list', 'create']
            show_action = ['retrieve', 'update', 'delete']
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
            setattr(self, 'serializer_class', getattr(
                __import__(serializer_path, globals(), locals(), [serializer_name], 0),
                serializer_name
            ))

    def autoload_template(self):
        if getattr(self, 'template_name', None) is None:

            def get_template_name_suffix(action):
                index_action = ['list', 'delete', 'create']
                show_action = ['retrieve', 'update']

                if action in index_action:
                    return ".list"
                elif action in show_action:
                    return ".detail"
                else:
                    return ".%s" % action
            
            def get_parent_resources_template_prefix(parent_resources):
                return reduce(
                    lambda model, cur: cur + "%s/" % model.lower(), 
                    parent_resources, ""
                )

            if hasattr(self, 'model'):
                opts = self.model._meta
                setattr(self, 'template_name', "%s/%s%ss%s.html" % (
                    opts.app_label, 
                    get_parent_resources_template_prefix(
                        self.get_parent_resources()
                    ),opts.model_name, 
                    get_template_name_suffix(self.action)
                ))
            else: # model이 없으면 에러 발생
                raise ImproperlyConfigured(
                    "%(cls)s requires either a 'template_name' attribute "
                    "or a get_queryset() method that returns a QuerySet." % {
                        'cls': self.__class__.__name__,
                    }
                )
    def autoload_paginator(self):
        if getattr(self, 'pagination_class', None) is None:
            parent_resources = self.get_parent_resources()
            resource = self.get_resource()

            paginator_path = "%s.paginators%s" % (
                self.request.resolver_match.app_name,
                reduce(
                    lambda path, cur: "." + path + cur.lower(), parent_resources, ""
                )
            )

            paginator_name = "%s_paginator" % resource
            paginator_path += ".%s" % paginator_name
            paginator_name = self.camelize_snake(paginator_name)

            try:
                setattr(self, 'pagination_class', getattr(
                    __import__(paginator_path, globals(), locals(), [paginator_name], 0),
                    paginator_name
                ))
            except:
                pass
    # def autoload_service(self):
    #     import logging
    #     service_path = "%s.services" % self.request.resolver_match.app_name
    #     service_dir_path = os.path.dirname(
    #         __import__(service_path, globals(), locals(), ['*']).__file__
    #     )
    #     service_files = [
    #         _file 
    #             for _file in os.listdir(service_dir_path) 
    #                 if os.path.isfile(os.path.join(service_dir_path, _file))
    #     ][1:]
    #     for _file in service_files:
    #         file_name = _file[:-3]
    #         service_class_name = self.camelize_snake(file_name)
    #         globals()[service_class_name] = getattr(
    #             __import__(
    #                 "%s.%s" % (service_path, file_name), 
    #                 globals(), locals(), [service_class_name]
    #             ), service_class_name
    #         )
    
    # get_queryset #
    def autoload_queryset(self):
        if getattr(self, 'queryset', None) is None:
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
                reference_object = get_object_or_404(parent_queryset, pk=pk)

            if reference_object is not None:
                queryset = queryset.filter(**{
                    reference_object_reference_name: reference_object
                })

            setattr(self, 'queryset', queryset)

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
