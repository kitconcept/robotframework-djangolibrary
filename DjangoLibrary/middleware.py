from django.contrib import auth
from django.contrib.auth.middleware import AuthenticationMiddleware
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
        args = request.GET.get('FACTORY_BOY_ARGS')
        args = json.loads(args)
        FactoryBoyClass = locate(model_name)
        user = FactoryBoyClass(**args)
        return JsonResponse({
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'args': args
        }, status=201)
