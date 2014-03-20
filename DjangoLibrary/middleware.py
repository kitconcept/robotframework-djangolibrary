from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.middleware import AuthenticationMiddleware

import base64


class AutologinAuthenticationMiddleware(AuthenticationMiddleware):

    def process_request(self, request):
        if not 'autologin' in request.COOKIES:
            return
        if request.COOKIES['autologin'] == '':
            logout(request)
            return
        autologin_cookie_value = base64.b64decode(request.COOKIES['autologin'])
        username = autologin_cookie_value.split(':')[0]
        password = autologin_cookie_value.split(':')[1]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
