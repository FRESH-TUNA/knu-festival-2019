"""레일즈 스타일의 BaseView 만들기

레일즈 프레임워크에서는 정해진 네이밍 규칙을 따르면 
컨트롤러에서 필요한 모듈을 자동으로 import 하는 
편리함을 가지고 있습니다. 또한 기본적으로 Restful한 
메소드 모두 지원해줍니다.

Django 에선 이기능들을 제공하지 않아 직접 한번 구현해봤습니다.
기존 GET, POST방식만 지원하는것과는 다르게 restful method를 
모두 지원하도록 설계했고 model, queryset, serializer, 
paginator, template을 네이밍 규칙에 따라 자동으로 로딩합니다.
따라서 추가적인 변경이 필요하지 않으면 get_queryset() 등의 메소드를
오버로딩 하지 않아도 됩니다.
다른 view class 에서 이 BaseView를 import 해서 사용하면 됩니다.

만약 커스텀한설정이 필요하다면 그부분을 overloading 하여 
사용하면 됩나다.
"""

"""네이밍 규칙 예제
예제1) GET, <app_name>/posts 에 해당하는 로직
1. <app_name>/models.py 에서 Post를 찾아 로딩
2. model의 정보를 바탕으로 posts/<post_pk>/comments 의 데이터들을 로딩
3. <app_name>/serializer/posts/comments_list_serializer.py 
   에서 CommentsListSerializer 클래스를 로딩
4. <app_name>/paginators/posts_paginator.py 에서 PostsPaginator 
   클래스를 로딩
5. <app_name>/templates/<app_name>/posts/comments.list.html
   을 랜더링

예제2) GET, <app_name>/posts/<post_pk>/comments 에 해당하는 로직
1. <app_name>/models.py 에서 Comment를 찾아 로딩
2. model의 정보를 바탕으로 posts/<post_pk>/comments 의 데이터들을 로딩
3. <app_name>/serializer/posts/comments_list_serializer.py 
   에서 CommentsListSerializer 클래스를 로딩
4. <app_name>/paginators/posts_paginator.py 에서 PostsPaginator 
   클래스를 로딩
5. <app_name>/templates/<app_name>/posts/comments.list.html
   을 랜더링
"""
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

    # put, delete 지원을 위한 overloading
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

    def autoload_model(self):
        if getattr(self, 'model', None) is None:
            try:
                setattr(self, 'model', self.get_model(self.get_resource()))
            except:
                pass
    
    def autoload_serializer(self):
        if getattr(self, 'serializer_class', None) is None:
            try:
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
            except:
                pass

    def autoload_template(self):
        if getattr(self, 'template_name', None) is None:
            try:
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
            except:
                pass

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
    
    # get_queryset #
    def autoload_queryset(self):
        try:
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
        except:
            pass

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
