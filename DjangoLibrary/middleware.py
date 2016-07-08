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

    def _get_foreign_key_fields(self, FactoryBoyClass):
        foreign_key_fields = []
        for field in FactoryBoyClass._meta.model._meta.fields:
            if isinstance(field, ForeignKey):
                foreign_key_fields.append(field)
        return foreign_key_fields

    def _foreign_key_to_model(self, FactoryBoyClass, factory_boy_args):
        if not hasattr(FactoryBoyClass, '_meta'):
            return
        if not hasattr(FactoryBoyClass._meta.model, '_meta'):
            return
        for field in self._get_foreign_key_fields(FactoryBoyClass):
            for key, value in factory_boy_args.items():
                key_name = '{}__pk'.format(field.name)
                if key == key_name:
                    RelModel = field.foreign_related_fields[0].model
                    del factory_boy_args[key_name]
                    new_key = key_name.replace('__pk', '')
                    factory_boy_args[new_key] = RelModel.objects.first()

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
        self._foreign_key_to_model(FactoryBoyClass, factory_boy_args)
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
        serialized_obj = model_to_dict(obj)
        serialized_obj['pk'] = obj.pk
        return JsonResponse(serialized_obj, status=201)


class QuerySetMiddleware():

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
        limit = None
        if 'limit' in query_args:
            limit = query_args['limit']
            del query_args['limit']
        offset = None
        if 'offset' in query_args:
            offset = query_args['offset']
            del query_args['offset']
        if query_args:
            try:
                objects = ModelClass.objects.filter(**query_args)
            except ModelClass.DoesNotExist:
                objects = []
        else:
            objects = ModelClass.objects.all()
        if offset and limit:
            objects = objects[int(offset):int(limit)]
        elif not offset and limit:
            objects = objects[:int(limit)]
        for obj in objects:
            serialized_obj = model_to_dict(obj)
            serialized_obj['pk'] = obj.pk
            result.append(serialized_obj)
        return JsonResponse(result, safe=False, status=200)
