import importlib
import re
import logging
from functools import reduce
from django.conf import settings
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from rest_framework.viewsets import GenericViewSet

from rest_framework.renderers import (
    TemplateHTMLRenderer,
    JSONRenderer
)

from rest_framework.mixins import (
    ListModelMixin, 
    RetrieveModelMixin, 
    CreateModelMixin, 
    UpdateModelMixin, 
    DestroyModelMixin
)

class BaseGenericViewSet(
    GenericViewSet, 
    ListModelMixin, 
    RetrieveModelMixin, 
    CreateModelMixin, 
    UpdateModelMixin, 
    DestroyModelMixin
):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    # queryset
    # serializer_class = PurposeSerializer
    # lookup_field = 'comment_pk'
    
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
            self.get_resources()[:-1], ""
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

    def get_resources(self):
        return re.sub(
            r'(?<!^)(?=[A-Z])', '_', self.__class__.__name__
        ).split("_")[:-2]

    def get_serializer_class(self):
        if self.serializer_class is not None:
            return super().get_serializer_class()

        resources = self.get_resources()

        serializer_path = "%s.serializers%s" % (
            self.request.resolver_match.app_name,
            reduce(
                lambda path, cur: "." + path + cur.lower(), resources, ""
            )
        )

        serializer_resources_name = reduce(
            lambda resource, cur: cur + resource, resources, ""
        )

        if self.action == 'list':
            serializer_name = "%sListSerializer" % serializer_resources_name
        else:
            serializer_name = "%sDetailSerializer" % serializer_resources_name
        return getattr(
            __import__(serializer_path, globals(), locals(), [serializer_name], 0),
            serializer_name
        )
