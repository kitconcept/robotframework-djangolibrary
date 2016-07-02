from django.contrib import auth
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.forms.models import model_to_dict
from django.db.models import ForeignKey
from django.http import JsonResponse
from pydoc import locate

import base64
import json


class AutologinAuthenticationMiddleware(AuthenticationMiddleware):

    def process_request(self, request):
        if 'autologin' not in request.COOKIES:
            return
        if request.COOKIES['autologin'] == '':
            auth.logout(request)
            return
        autologin_cookie_value = base64.b64decode(request.COOKIES['autologin'])
        # Py3 uses a bytes string here, so we need to decode to utf-8
        autologin_cookie_value = autologin_cookie_value.decode('utf-8')
        username = autologin_cookie_value.split(':')[0]
        password = autologin_cookie_value.split(':')[1]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)


class FactoryBoyMiddleware():

    def process_request(self, request):
        model_name = request.GET.get('FACTORY_BOY_MODEL_PATH')
        if not model_name:
            return
        get_args = request.GET.get('FACTORY_BOY_ARGS')
        try:
            factory_boy_args = json.loads(get_args)
        except ValueError:
            factory_boy_args = {}
        FactoryBoyClass = locate(model_name)
        if not FactoryBoyClass:
            msg = 'Factory Boy class "{}" could not be found'
            return JsonResponse(
                {
                    'error': msg.format(model_name)
                },
                status=400
            )
        # XXX: experiemental and ugly proof-of-concept code
        if hasattr(FactoryBoyClass, '_meta'):
            if hasattr(FactoryBoyClass._meta.model, '_meta'):
                for field in FactoryBoyClass._meta.model._meta.fields:
                    if isinstance(field, ForeignKey):
                        for key, value in factory_boy_args.items():
                            key_name = '{}__pk'.format(field.name)
                            if key == key_name:
                                RelModel = field.foreign_related_fields[0].model
                                del factory_boy_args[key_name]
                                new_key = key_name.replace('__pk', '')
                                factory_boy_args[new_key] = RelModel.objects.first()
        try:
            obj = FactoryBoyClass(**factory_boy_args)
        except:
            return JsonResponse(
                {
                    'error': 'FactoryBoyClass "{}" '.format(model_name) +
                    'could not be instantiated with args "{}"'.format(
                        factory_boy_args
                    )
                },
                status=400
            )
        obj_meta = getattr(obj, '_meta', None)
        if not obj_meta:
            return JsonResponse(
                {
                    'error': 'The FactoryBoyClass "{}" '.format(model_name) +
                    'instance does not seem to provide a _meta attribute. ' +
                    'Please check if the Factory Boy class inherits from ' +
                    'DjangoModelFactory'
                },
                status=400
            )
        return JsonResponse(model_to_dict(obj), status=201)


class QueryMiddleware():

    def process_request(self, request):
        model_name = request.GET.get('MODEL_PATH')
        if not model_name:
            return
        get_args = request.GET.get('QUERY_ARGS')
        try:
            query_args = json.loads(get_args)
        except (ValueError, TypeError):
            query_args = {}
        ModelClass = locate(model_name)
        if not ModelClass:
            msg = 'Class "{}" could not be found'
            return JsonResponse(
                {
                    'error': msg.format(model_name)
                },
                status=400
            )
        result = []
        if query_args:
            try:
                objects = [ModelClass.objects.get(**query_args)]
            except ModelClass.DoesNotExist:
                objects = []
        else:
            objects = ModelClass.objects.all()
        for obj in objects:
            result.append(
                model_to_dict(obj)
            )
        return JsonResponse(result, safe=False, status=200)
